from curses import window
import PySimpleGUI as sg

theme_style = 'reddit'
theme_button_text = 'Change to Dark Mode'
actions = []

path = 'resources/no_img_loaded.png'
scale = str(120)
contrast = str(0)
depth = str(6)

def add_to_actions(cur_scale, cur_contrast, cur_depth):
    actions.append([cur_scale, cur_contrast, cur_depth])

def make_window():
    sg.theme(theme_style)
    sliders = sg.Column([
        [sg.Frame('Resolution', font='80', size=(300,70), layout=[[sg.Slider(range = (50,200), font='80', orientation='h', key='-RESOLUTION-', default_value=int(scale), size=(300,30))]])],
        [sg.Frame('Contrast', font='80', size=(300,70), layout=[[sg.Slider(range = (-10,10), font='80', orientation='h', key='-CONTRAST-', default_value=int(contrast), size=(300,30))]])],
        [sg.Frame('Depth', font='80', size=(300,70), layout=[[sg.Slider(range = (2,11), font='80', orientation='h', key='-DEPTH-', default_value=int(depth), size=(300,30))]])]
    ])
    buttons = sg.Column([
        [sg.Frame("Current Image Path", font='80', layout=[
            [sg.Text("No Image Selected!", key='-DIRPATH-', font='70')]
        ])],
        [sg.Button('LOAD IMAGE', key='-LOAD-', font='80', expand_x=True), sg.Button('SAVE ASCII', key='-SAVE-', font='80', expand_x=True)],
        [sg.Frame('Options', font='80', size=(200,125), layout=[
            [sg.Button('Reset', key='-RESET-', font='80', expand_x=True), sg.Checkbox('Protect', key='-PROTECTRESET-', font='50')],
            [sg.Button('Undo', key='-UNDO-', font='80', expand_x=True), sg.Checkbox('Protect', key='-PROTECTUNDO-', font='50')],
            [sg.Button('Random', key='-RANDOM-', font='80', expand_x=True), sg.Checkbox('Protect', key='-PROTECTRANDOM-', font='50')]
            ])]
    ])
    layout = [
        [
            sg.Image('resources/top_logo.png'), 
            sg.Button(theme_button_text, key="-CHANGETHEME-", font='100', expand_x=True),
            sg.Button('Close Program', key="-CLOSEPROGRAM-", font='100', expand_x=True)
            ],
        [sliders, buttons]
        ]
    return sg.Window("Image-to-ASCII Converter", layout, finalize=True)

window = make_window()
window['-RESOLUTION-'].bind('<ButtonPress-1>', ' Release')
window['-CONTRAST-'].bind('<ButtonPress-1>', ' Release')
window['-DEPTH-'].bind('<ButtonPress-1>', ' Release')

# check if rng and ascii microservices are running
ascii_comms = open('text_comm/ascii.txt', 'r+')
if ascii_comms.readline().strip() == 'Not Running':
    sg.popup("ASCII conversion service is down.")
ascii_comms.close()
comms = open('text_comm/rng.txt', 'r+')
if comms.readline().strip() == 'Not Running':
    sg.popup("RNG service is down.")
comms.close()
display_comms = open('text_comm/display.txt', 'r+')
if display_comms.readline().strip() == 'Not Running':
    sg.popup("Display service is down.")
display_comms.close()


while True:
    event, values = window.read(timeout=0)

    if values:
        scale = str(int(values['-RESOLUTION-']))
        contrast = str(int(values['-CONTRAST-']))
        depth = str(int(values['-DEPTH-']))

    if event == sg.WIN_CLOSED:
        break

    if event == '-CHANGETHEME-':
        if theme_style == 'reddit':
            theme_style = 'DarkBlue'
            theme_button_text = 'Change to Light Mode'
            window.close()
            window = make_window()
            window['-RESOLUTION-'].bind('<ButtonPress-1>', ' Release')
            window['-CONTRAST-'].bind('<ButtonPress-1>', ' Release')
            window['-DEPTH-'].bind('<ButtonPress-1>', ' Release')
        else:
            theme_style = 'reddit'
            theme_button_text = 'Change to Dark Mode'
            window.close()
            window = make_window()  
            window['-RESOLUTION-'].bind('<ButtonPress-1>', ' Release')
            window['-CONTRAST-'].bind('<ButtonPress-1>', ' Release')
            window['-DEPTH-'].bind('<ButtonPress-1>', ' Release')
    
    if event == "-CLOSEPROGRAM-":
        choice = sg.popup_ok_cancel("Close Program?")
        if choice == 'OK':
            break

    if event == '-LOAD-':
        img_path = sg.popup_get_file('Open', no_window=True, file_types=(('PNG', '.png'),('JPG', '.jpg')))
        path = img_path
        window['-DIRPATH-'].update(path)

    if event == '-SAVE-':
        save_path = sg.popup_get_file('Save', save_as=True, no_window=True) + '.txt'
        new_file = open(save_path, 'w')
        ascii_file = open('text_comm/ascii_output.txt', 'r+')
        ascii_lines = ascii_file.readlines()
        for line in ascii_lines:
            new_file.write(line)
        ascii_file.close()
        new_file.close()

    if event == '-RESOLUTION- Release' or event == '-CONTRAST- Release' or event == '-DEPTH- Release':
        add_to_actions(int(values['-RESOLUTION-']), int(values['-CONTRAST-']), int(values['-DEPTH-']))

    if event == '-RESET-':
        update = True
        if values['-PROTECTRESET-'] == True:
            if sg.popup_ok_cancel("Reset values to starting values?") != 'OK':
                update = False
        if update == True:
            add_to_actions(int(values['-RESOLUTION-']), int(values['-CONTRAST-']), int(values['-DEPTH-']))
            window['-RESOLUTION-'].update(120)
            window['-CONTRAST-'].update(0)
            window['-DEPTH-'].update(6)
    
    if event == '-UNDO-':
        update = True
        if values['-PROTECTUNDO-'] == True:
            if sg.popup_ok_cancel("Undo last adjustment?") != 'OK':
                update = False
        if update == True:
            if len(actions) < 1:
                sg.popup("No more actions to undo!")
            else:
                undo_vals = actions.pop()
                window['-RESOLUTION-'].update(undo_vals[0])
                window['-CONTRAST-'].update(undo_vals[1])
                window['-DEPTH-'].update(undo_vals[2])

    if event == '-RANDOM-':
        update = True
        if values['-PROTECTRANDOM-'] == True:
            if sg.popup_ok_cancel("Randomize all sliders?") != 'OK':
                update = False
        if update == True:
            comms = open('text_comm/rng.txt', 'r+')
            comms_lines = comms.readlines()
            if len(comms_lines) > 0 and comms_lines[0].strip() == 'Running':
                add_to_actions(int(values['-RESOLUTION-']), int(values['-CONTRAST-']), int(values['-DEPTH-']))
                window['-RESOLUTION-'].update(comms_lines[1].strip())
                window['-CONTRAST-'].update(comms_lines[2].strip())
                window['-DEPTH-'].update(comms_lines[3].strip())
                comms.truncate(0)
                comms.writelines("Running\n" + "Retrieved")
            else:
                sg.popup("RNG service is down.")
            comms.close()

    var_list = [path + "\n", scale + "\n", contrast + "\n", depth + "\n"]
    var_txt = open('text_comm/vars.txt', 'w')
    var_txt.truncate(0)
    var_txt.writelines(var_list)
    var_txt.close()


comms = open('text_comm/rng.txt', 'r+')
comms_lines = comms.readlines()
if comms_lines[0].strip() == 'Running':
    comms.seek(0)
    comms.truncate()
    comms.writelines("Running\n" + "Stop")
comms.close()

ascii_comms = open('text_comm/ascii.txt', 'r+')
if ascii_comms.read().strip() == 'Running':
    ascii_comms.seek(0)
    ascii_comms.truncate()
    ascii_comms.write("Stop")
ascii_comms.close()

display_comms = open('text_comm/display.txt', 'r+')
if display_comms.read().strip() == 'Running':
    display_comms.seek(0)
    display_comms.truncate()
    display_comms.write("Stop")
display_comms.close()

window.close()
