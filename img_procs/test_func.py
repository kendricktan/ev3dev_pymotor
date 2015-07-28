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

# Phase 1 of 2
client.send('us_avoid_object_1')

# Allows command to finish running
time.sleep(5)

# before aligning to horizontal line
# always set is_aligned_hori to false
pi_img_procs.set_is_aligned_hori(False)
while not pi_img_procs.is_aligned_hori:
    # align_horizontal_line accepts a boolean parameter
    # True if going backwards
    # False if going forwards
    pi_img_procs.align_horizontal_line(True)
    client.send(pi_img_procs.get_rmotor_cmd())
    client.send(pi_img_procs.get_lmotor_cmd())

time.sleep(0.5)

# Phase 2 of 2
client.send('us_avoid_object_2')

# Waits for command to complete
time.sleep(8)

# Resets PID value to prevent random movement
pi_img_procs.reset_PID()

