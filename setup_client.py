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

            # We want slower speed
            while obj_dist > US_MIN_DIST and obj_dist <= US_START_DIST:
                pi_img_procs.update()

                client.send('right change_rps('+str(pi_img_procs.get_rmotor_value()/3)+')')
                client.send('left change_rps('+str(pi_img_procs.get_lmotor_value()/3)+')')

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

    # Does it detect a greenbox
    if pi_img_procs.get_is_greenbox():
        # Gets greenbox location
        greenbox_location = pi_img_procs.get_greenbox_location()

        # Goes slowly along blackline until passes the greenbox
        while pi_img_procs.get_is_greenbox():
            pi_img_procs.update()
            client.send('right change_rps('+str(math.ceil(pi_img_procs.get_rmotor_value()/3*100)/100)+')')
            client.send('left change_rps('+str(math.ceil(pi_img_procs.get_lmotor_value()/3*100)/100)+')')

        time.sleep(0.075)

        # Starts over the blackline (if any)
        # Sleep helps provide consistent packet sending
        client.send('stop')
        time.sleep(0.075)
        client.send('set_rps(0.75)')
        time.sleep(0.075)
        client.send('run_to_rel_pos(145)')
        time.sleep(1)
        client.send('stop')
        time.sleep(0.075)

        # Sends robot in direction of the greenbox
        if 'left' in greenbox_location:
            client.send('left change_rps(-0.25)')
            time.sleep(0.075)
            client.send('right change_rps(0.25)')

        elif 'right' in greenbox_location:
            client.send('right change_rps(-0.25)')
            time.sleep(0.075)
            client.send('left change_rps(0.25)')

        # This is merely a pattern formed in robocup 2015
        # that we're taking advantage of
        while pi_img_procs.get_is_detected_black_line():
            pi_img_procs.update()

        while not pi_img_procs.get_is_black_line_straight():
            pi_img_procs.update()

        client.send('stop')

    # Updates camera feed
    pi_img_procs.update()

    # Rotates motor according to camera feed
    client.send(pi_img_procs.get_rmotor_cmd())
    client.send(pi_img_procs.get_lmotor_cmd())
