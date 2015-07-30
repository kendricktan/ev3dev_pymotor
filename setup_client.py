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
pi_img_procs.print_cmd(True)

# uncomment if you want to show gui
#pi_img_procs.show_gui(True)

# Initialize Ultrasonic sensor class
us_sens01 = us_read(14, 15)

# Get current start time
start_time = time.time()

while True:
    # Take an ultrasonic sensor reading
    if time.time()-start_time >= 0.05:
        # takes reading
        obj_dist = us_sens01.read()

        start_time = time.time()

        # If we detect some object nearby ....
        if obj_dist <= US_START_DIST:
            while obj_dist > US_MIN_DIST and obj_dist <= US_START_DIST:
                pi_img_procs.update()

                # We want slower speed now...
                client.send('right change_rps('+ str(pi_img_procs.get_rmotor_value()/3) +')')
                client.send('left change_rps('+ str(pi_img_procs.get_lmotor_value()/3) +')')

                obj_dist = us_sens01.read()
                time.sleep(0.01)

            if obj_dist <= US_MIN_DIST:
                # Safety check
                time.sleep(0.25)
                client.send('stop')
                time.sleep(0.25)

                # Special command to avoid
                # objects detected by ultrasonic sensor
                client.send('us_avoid_object')

                # Allows command to finish running
                time.sleep(12.5)

                # Resets PID value to prevent random movement
                pi_img_procs.reset_PID()

                # Just for safety
                time.sleep(1.0)

    # Updates camera feed
    pi_img_procs.update()

    # If we're moved towards the end of a greenbox we'll shout a special command
    if pi_img_procs.get_is_greenbox():

        if 'left' in pi_img_procs.get_greenbox_location():
            client.send('anticlockwise_90')
        elif 'right' in pi_img_procs.get_greenbox_location():
            client.send('clockwise_90')

        # Resets boolean var that indicates
        # We've found the greenbox
        pi_img_procs.reset_green_hzone()

        # Wait till command finishes executing
        time.sleep(5)

    # Rotates motor according to camera feed
    client.send(pi_img_procs.get_rmotor_cmd())
    client.send(pi_img_procs.get_lmotor_cmd())

    time.sleep(0.01)
