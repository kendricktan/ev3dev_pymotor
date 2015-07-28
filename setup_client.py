from ev3dev_pymotor.ev3dev_pymotor import *
from img_procs.img_procs import *
from us_read.us_read import *
from tcp.client import *
import time

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

print 'Successfully connected to ' + TCP_IP +  '...'

# Initialize image processing class
pi_img_procs = img_procs()

# comment if you want to print the commands
pi_img_procs.print_cmd(False)

# uncomment if you want to show gui
#pi_img_procs.show_gui(True)

# Initialize Ultrasonic sensor class
us_sens01 = us_driver(14, 15)

# Get current start time
start_time = time.time()

while True:
    # Take an ultrasonic sensor reading
    if time.time()-start_time >= 0.05:
        # takes reading
        obj_dist = us_sens01.read()

        start_time = time.time()

        if obj_dist <= US_MIN_DIST:
            # Special command to avoid
            # objects detected by ultrasonic sensor

            # Phase 1 of 2
            client.send('us_avoid_object_1')

            # Allows command to finish running
            time.sleep(5)

            # before aligning to horizontal line
            while not pi_img_procs.is_aligned:
                pi_img_procs.align_horizontal_line(False)
                client.send(pi_img_procs.get_rmotor_cmd())
                client.send(pi_img_procs.get_lmotor_cmd())

            time.sleep(0.5)

            # Phase 2 of 2
            client.send('us_avoid_object_2')

            # Waits for command to complete
            time.sleep(8)

            # Resets PID value to prevent random movement
            pi_img_procs.reset_PID()

    # Updates camera feed
    pi_img_procs.update()

    # Rotates motor according to camera feed
    client.send(pi_img_procs.get_rmotor_cmd())
    client.send(pi_img_procs.get_lmotor_cmd())

    time.sleep(0.01)
