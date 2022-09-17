import PySimpleGUI as sg

layout = [
    [sg.Multiline(key='-DISPLAY-', size=(200,100), font='Courier')]
    ]

window = sg.Window("ASCII Render", layout)

display_comms = open("text_comm/display.txt", "w")
display_comms.truncate(0)
display_comms.write('Running\n')
display_comms.close()


while True:
    event, values = window.read(timeout=0)

    display_comms = open("text_comm/display.txt", "r")
    display_lines = display_comms.readlines()
    if len(display_lines) > 0:
        if display_lines[0].strip() == "Stop":
            display_comms.close()
            break

    ascii_file = open('text_comm/ascii_output.txt', 'r')
    ascii_img = ascii_file.read()
    window['-DISPLAY-'].update(ascii_img)
    ascii_file.close()

    if event == sg.WIN_CLOSED:
        break


display_comms = open('text_comm/display.txt', 'r+')
if display_comms.readline().strip() == "Stop":
    display_comms.seek(0)
    display_comms.truncate()
    display_comms.write("Not Running")
display_comms.close()

window.close()

