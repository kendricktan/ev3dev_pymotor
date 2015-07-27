from img_procs import *

# Initalizes tcp connection
# Checks for usage help
if len(sys.argv) > 1:
    if sys.argv[1] == '-h' or sys.argv[1] == '--help':
        print 'Usage: python setup_client.py [server ip]'
        sys.exit()

TCP_PORT = 5005
TCP_IP = str(sys.argv[1]) if len(sys.argv) > 1 else ''
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((TCP_IP, 5005))

# Initialize image processing class
pi_img_procs = img_procs()

time.sleep(0.5)

# Rotate 90 degrees
client.send('left run_to_rel_pos(-215)')
time.sleep(0.05)
client.send('right run_to_rel_pos(215)')

time.sleep(1.85)

# Goes up ahread
client.send('run_to_rel_pos(150)')

time.sleep(0.5)

# Realigns with horizontal light
# Needs to set to false before initiating this function
pi_img_procs.set_is_aligned_hori(False)
while not pi_img_procs.is_aligned_hori:
    pi_img_procs.align_horizontal_line(True)

    client.send(pi_img_procs.get_rmotor_cmd())
    client.send(pi_img_procs.get_lmotor_cmd())

time.sleep(0.5)

# Circulates object
client.send('left change_rps(0.81)')
client.send('right change_rps(0.4)')

time.sleep(4.25)

# Realigns with line
pi_img_procs.set_is_aligned_hori(False)
while not pi_img_procs.is_aligned_hori:
    pi_img_procs.align_horizontal_line(False)

    client.send(pi_img_procs.get_rmotor_cmd())
    client.send(pi_img_procs.get_lmotor_cmd())

time.sleep(0.5)

# Turns 90 degrees
client.send('left run_to_rel_pos(-215)')
time.sleep(0.05)
client.send('right run_to_rel_pos(215)')

time.sleep(1.85)

client.send('stop')
client.send('stop')

