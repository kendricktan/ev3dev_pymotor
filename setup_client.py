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

# if you don't want it to print the commands
pi_img_procs.print_cmd(False)
# if you want to show gui
#pi_img_procs.show_gui(True)

# Initialize Ultrasonic sensor class
us_sens01 = us_driver(14, 15)

start_time = time.time()

while True:
    # Take an ultrasonic sensor reading
    # every half a second (?)
    if time.time()-start_time >= 0.05:
        # takes reading
        obj_dist = us_sens01.read()
        print obj_dist

        start_time = time.time()

        if obj_dist <= US_MIN_DIST:
            print 'object detected!'
            client.send('stop')
            client.send('quit')
            break

            # Theory is that if detect changes then we wait for 2 sec and read again
            # (Maybe stop robot while doing it
            # As in reverse and wait 1 second and retake reading

    pi_img_procs.update()

    client.send(pi_img_procs.get_rmotor_cmd())
    client.send(pi_img_procs.get_lmotor_cmd())

    time.sleep(0.01)
