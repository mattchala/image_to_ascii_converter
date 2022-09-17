import random

def generate_vals():
    random.seed()
    scale = str(random.randint(50, 200))
    contrast = str(random.randint(-10, 10))
    depth = str(random.randint(2, 11))
    var_list = ["Running\n" + scale + "\n", contrast + "\n", depth + "\n"]
    comms = open('text_comm/rng.txt', 'r+')
    comms.truncate(0)
    comms.writelines(var_list)
    comms.close()

generate_vals()

while True:
    comms = open('text_comm/rng.txt', 'r+')
    comms_lines = comms.readlines()
    if len(comms_lines) > 0:
        if comms_lines[1].strip() == 'Retrieved':
            generate_vals()
        if comms_lines[1].strip() == 'Stop':
            break
    comms.close()

comms = open('text_comm/rng.txt', 'r+')
comms.truncate(0)
comms.write('Not Running')
comms.close()
