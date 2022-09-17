from PIL import Image, ImageFilter
import time

chars = ["@", "#", "$", "%", "?", "*", "+", ";", ":", ",", "."]
char_div = 25

def set_shade(num):
    global chars
    global char_div
    if num == 11:
        chars = ["@", "#", "$", "%", "?", "*", "+", ";", ":", ",", "."]
        char_div = 25
    if num == 10:
        chars = ["@", "$", "%", "?", "*", "+", ";", ":", ",", "."]
        char_div = 27
    if num == 9:
        chars = ["@", "$", "%", "?", "*", ";", ":", ",", "."]
        char_div = 30 
    if num == 8:
        chars = ["@", "$", "%", "?", "*", ";", ",", "."]
        char_div = 35
    if num == 7:
        chars = ["@", "$", "%", "?", "*", ";", "."]
        char_div = 40
    if num == 6:
        chars = ["@", "%", "?", "*", ";", "."]
        char_div = 50
    if num == 5:
        chars = ["@", "%", "?", ";", "."]
        char_div = 60
    if num == 4:
        chars = ["@", "?", ";", "."]
        char_div = 65
    if num == 3:
        chars = ["@", "?", "."]
        char_div = 90
    if num == 2:
        chars = ["@", "."]
        char_div = 140

def resize(image, new_width):
    stretch_correction = 0.55
    width, height = image.size
    new_height = new_width * height / width * stretch_correction
    new_height = int(new_height)
    return image.resize((new_width, new_height))
 
def make_gray(image):
    return image.convert("L")

def to_ascii_str(image):
    pix = image.getdata()
    ascii_str = ""
    for p in pix:
        ascii_str += chars[p//char_div] 
    return ascii_str

def add_new_lines(ascii_str, img_width):
    new_txt_img = ""
    str_len = len(ascii_str)
    for i in range(0, str_len, img_width):
        new_txt_img += ascii_str[i : i + img_width] + "\n"
    return new_txt_img

def set_contrast(image, value):
    return image.filter(ImageFilter.UnsharpMask(value))

ascii_comms = open("text_comm/ascii.txt", "w")
ascii_comms.truncate(0)
ascii_comms.write('Running\n')
ascii_comms.close()

# initialize vals
path = ""
scale_val = 10
contrast_val = 0
shade_val = 0

while True:
    time.sleep(0.25)

    # shuts down program if condition met
    ascii_comms = open("text_comm/ascii.txt", "r")
    ascii_lines = ascii_comms.readlines()
    if len(ascii_lines) > 0:
        if ascii_lines[0].strip() == "Stop":
            ascii_comms.close()
            break

    # get vars from txt
    var_txt = open("text_comm/vars.txt", "r+")
    var_lines = var_txt.readlines()
    if len(var_lines) > 0:
        path = var_lines[0].strip()
        scale_val = int(var_lines[1].strip())
        contrast_val = int(var_lines[2].strip())
        shade_val = int(var_lines[3].strip())
    var_txt.close()

    if path != "":
        image = Image.open(path)
    else:
        image = Image.open('resources/no_img_loaded.png') 

    image = resize(image, scale_val)   
    grey_image = make_gray(image)
    grey_image = set_contrast(grey_image, contrast_val)
    set_shade(shade_val)  
    ascii_str = to_ascii_str(grey_image)
    ascii_image = add_new_lines(ascii_str, grey_image.width) 

    # write result to file
    with open("text_comm/ascii_output.txt", "w") as output:
        output.write(ascii_image)
    output.close()

# change comms file on shut down
ascii_comms = open('text_comm/ascii.txt', 'r+')
if ascii_comms.readline().strip() == "Stop":
    ascii_comms.seek(0)
    ascii_comms.truncate()
    ascii_comms.write("Not Running")
ascii_comms.close()
