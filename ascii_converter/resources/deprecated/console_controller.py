import random

while True:

    path = input("Enter directory path to image: \n")
    scale = str(100)
    contrast = str(2)
    depth = str(6)

    print("Now select one of the following options:\n")

    choice = input("Generate an image with recommended settings - quick & easy (enter '1')\nEdit parameters yourself - if you're confident and creative (enter '2')?\nRandomize parameters - if you're feeling adventurous (enter '3')\n\nYour choice: ")

    if choice == "2":
        print("\nEnter image modifier values, they will not change the original file\n")
        scale = input("Enter scale (50 to 200): \n")
        contrast = input("Enter contrast (-10 to 10): \n")
        depth = input("Enter shading depth (2 t0 11): \n")

    # needs input validation, then translate this to an actual GUI w/ PySimpleGUI

        submit = input("Would you like to submit these choices? Y/N \n")

        if submit == "Y":
            var_list = [path + "\n", scale + "\n", contrast + "\n", depth + "\n"]
            var_txt = open('vars.txt', 'w')
            var_txt.truncate(0)
            var_txt.writelines(var_list)
            var_txt.close()
            print("\n\ncheck the ascii.txt file for your result!\n\n")
        else:
            print("Variables not submitted")
            continue
    
    elif choice == "1":
        var_list = [path + "\n", scale + "\n", contrast + "\n", depth + "\n"]
        var_txt = open('vars.txt', 'w')
        var_txt.truncate(0)
        var_txt.writelines(var_list)
        var_txt.close()
        print("\n\ncheck the ascii.txt file for your result!\n\n")
    
    else: # choice == "3"
        random.seed()
        scale = str(random.randint(50, 200))
        contrast = str(random.randint(-10, 10))
        depth = str(random.randint(2, 11))
        var_list = [path + "\n", scale + "\n", contrast + "\n", depth + "\n"]
        var_txt = open('vars.txt', 'w')
        var_txt.truncate(0)
        var_txt.writelines(var_list)
        var_txt.close()
        print("\n\ncheck the ascii.txt file for your result!\n\n")

    try_again = input("Would you like to try again? Y/N \n")

    if try_again == "Y":
        continue
    else:
        break
