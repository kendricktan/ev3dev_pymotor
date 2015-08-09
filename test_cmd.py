from ev3dev_pymotor.ev3dev_pymotor import *
from img_procs.img_procs import *
from us_read.us_read import *
from tcp.client import *
from servo.servo_driver import *
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

servo=servo_driver(4)
servo.degrees_0()
time.sleep(0.5)
servo.degrees_180()
time.sleep(0.5)
servo.degrees_0()
time.sleep(0.5)

start_time = time.time()

# Set initial rps
client.send('set_rps(0.65')
client.send('run_forever')

# Goes straight until it's within 15cm of the platform
while us_sens01.get_lowest_reading() >= 15:
    pass

client.send('stop')
time.sleep(0.25)

# Turn 180 degrees
client.send('degrees_180')
time.sleep(4)

# Begin turning clockwise slowly
client.send('clockwise_slow')

time.sleep(0.6)

# Until we found an object we'll keep moving
dist = us_sens01.get_lowest_reading()
while dist > 25:
    dist = us_sens01.get_lowest_reading()

# Go forward to grab object
client.send('left change_rps(0.25)')
client.send('right change_rps(0.25)')

while True:
    dist = us_sens01.get_lowest_reading()

    # Object is beyong sight, needa recalibrate
    if dist > 25:
        # Turn right a bit
        client.send('crane_nudge_right')
        time.sleep(0.7)

        dist = us_sens01.get_lowest_reading()
        # If still not within sight, then turn other direction
        if dist > 15:
            client.send('crane_s_nudge_left')

        else:
            client.send('stop')
            break

    # Found object
    elif dist <= 5:
        client.send('stop')
        break

print 'found object!'
client.send('stop')
time.sleep(0.1)
client.send('can_detected')
time.sleep(12.5)
servo.degrees_180()
time.sleep(0.5)
client.send('crane run_to_rel_pos(1750)')
time.sleep(8)

