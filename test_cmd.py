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

# Calibrates servo
servo=servo_driver(4)
servo.degrees_0()
time.sleep(4)

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
time.sleep(3.5)

# Begin turning clockwise slowly
client.send('clockwise_slow')

time.sleep(0.6)

# Takes around 5.6 seconds to rotate 180 degrees
# with 0.25 rps
# Use this to calculate ~ how much to turn later

start_turn_time = time.time()

# Until we found an object we'll keep moving
while us_sens01.get_lowest_reading() > 25:
    pass

end_turn_time = time.time()

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

# Proceeding steps to drop can at platform
client.send('stop')
time.sleep(0.1)

# Positions servo to grab can
client.send('can_detected')
time.sleep(12.5)

# Actually grabs can
servo.degrees_180()
time.sleep(0.5)

# Pull cna up
client.send('crane run_to_rel_pos(1750)')
time.sleep(8)

# Reverses the robot
client.send('reverse_short')
time.sleep(2.5)

# Turn clockwise until it finds the platform
# based on timing :\
rotate_time = 5-(end_turn_time-start_turn_time)

start_turn_time = time.time()

client.send('clockwise_slow')

while time.time()-start_turn_time <= rotate_time:
    pass

client.send('stop')

# Go forward until reaches platform
client.send('change_rps(0.35)')

# 4 seconds should be enough
time.sleep(4)

client.send('stop')

# Reverses a little bit
client.send('run_to_rel_pos(-85)')
time.sleep(1)

# Drops can
servo.degrees_0()

time.sleep(2)

client.send('change_rps(-0.75)')
