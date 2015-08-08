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
client = client_tcp(TCP_IP)

print 'Successfully connected to ' + TCP_IP +  '...'

# Initialize Ultrasonic sensor class
us_sens01 = us_read(14, 15)

start_time = time.time()

# get platform dist
platform_dist = us_sens01.get_lowest_reading()

# Turn 180 degrees
client.send('left run_to_rel_pos(-485)')
client.send('right run_to_rel_pos(485)')

time.sleep(4)

# Begin turn
client.send('left change_rps(0.25)')
client.send('right change_rps(-0.25)')

time.sleep(0.1)

# Gets distance to voidness

dist = us_sens01.get_lowest_reading()

# Until we found an object we'll keep moving
while abs(platform_dist-dist) > 15:
    dist = us_sens01.get_lowest_reading()

# Go forward to grab object
client.send('left change_rps(0.25)')
client.send('right change_rps(0.25)')

while True:
    dist = us_sens01.get_lowest_reading()

    # Object is beyong sight, needa recalibrate
    if abs(platform_dist-dist) > 15:
        # Turn right a bit
        client.send('right run_to_rel_pos(-50)')
        client.send('left run_to_rel_pos(50)')

        time.sleep(0.7)

        dist = us_sens01.get_lowest_reading()

        # Change 15 to something else
        if abs(platform_dist-dist) > 15:
            client.send('right run_to_rel_pos(-100)')
            client.send('left run_to_rel_pos(100)')
            time.sleep(0.7)

        else:
            print 'found object!'

    elif dist <= 5:
        print 'in front of object!'
        client.send('stop')
        break


client.send('stop')
