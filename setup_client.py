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

# Initialize image processing class
pi_img_procs = img_procs()

# comment if you want to print the commands
pi_img_procs.print_cmd(False)

# uncomment if you want to show gui
#pi_img_procs.show_gui(True)

# Initialize Ultrasonic sensor class
us_sens01 = us_read(14, 15)

# Initialize and calibrates servo
servo = servo_driver(4)
servo.degrees_0()
time.sleep(1)

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

                # Allow it time to slowly follow blackline
                us_avoid_end = time.time()
                while time.time()-us_avoid_end <= 2.5:
                    pi_img_procs.update()
                    client.send('right change_rps('+str(pi_img_procs.get_rmotor_value()/3)+')')
                    client.send('left change_rps('+str(pi_img_procs.get_lmotor_value()/3)+')')

    # Does it detect aluminium foil (endzone)
    if pi_img_procs.get_is_aluminium_found():
        # Repositions itself so its straight
        alum_detect_time = time.time()

        while time.time()-alum_detect_time < 2:
            pi_img_procs.update()
            # Motor values are inverted as we're travelling backwards
            client.send('right change_rps(-'+str(math.ceil(pi_img_procs.get_lmotor_value()/3*100)/100)+')')
            client.send('left change_rps(-'+str(math.ceil(pi_img_procs.get_rmotor_value()/3*100)/100)+')')


        client.send('stop')
        # Recalibrates servo
        servo.degrees_0()
        time.sleep(0.25)

        # Set initial rps
        client.send('set_rps(0.65)')
        client.send('run_forever')

        # Goes straight until it's within 15cm of the platform
        while us_sens01.get_lowest_reading() >= 15:
            pass

        client.send('stop')
        time.sleep(0.25)

        # If can is not in extended zone
        if not EXTENDED_ZONE:
            # Turn 180 degrees
            client.send('degrees_180')
            time.sleep(3.5)

        # if can is in extended zone
        elif EXTENDED_ZONE:
            # Turn 90 degrees based on where can is
            if 'left' in EXTENDED_ZONE_LOCATION:
                client.send('right run_to_rel_pos(230)')
                time.sleep(0.125)
                client.send('left run_to_rel_pos(-230)')

            elif 'right' in EXTENDED_ZONE_LOCATION:
                client.send('right run_to_rel_pos(-230)')
                time.sleep(0.125)
                client.send('left run_to_rel_pos(230)')

            time.sleep(2)

            # Run to center of tile
            client.send('run_to_rel_pos(1200)')
            time.sleep(6.5)

        # Begin turning anti-clockwise/clockwise slowly based on can's position
        if not EXTENDED_ZONE:
            if 'left' in CAN_RELATIVE_POSITION:
                client.send('clockwise_slow')
            elif 'right' in CAN_RELATIVE_POSITION:
                client.send('clockwise_anti_slow')

        elif EXTENDED_ZONE:
            if 'left' in CAN_RELATIVE_POSITION:
                client.send('clockwise_anti_slow')
            elif 'right' in CAN_RELATIVE_POSITION:
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
                if 'left' in CAN_RELATIVE_POSITION:
                    # Turn right a bit
                    client.send('crane_nudge_right')
                    time.sleep(0.7)

                    dist = us_sens01.get_lowest_reading()
                    # If still not within sight, then turn other direction
                    if dist > 15:
                        client.send('crane_s_nudge_left')

                elif 'right' in CAN_RELATIVE_POSITION:
                    # Turn left a bit
                    client.send('crane_nudge_left')
                    time.sleep(0.7)

                    dist = us_sens01.get_lowest_reading()

                    # if still not within sight, then turn other direction
                    if dist > 15:
                        client.send('crane_s_nudge_right')

            # Found object
            elif dist <= 5:
                client.send('stop')
                break

        # Proceeding steps to grab can
        client.send('stop')
        time.sleep(0.1)

        # Positions servo to grab can
        client.send('can_detected')
        time.sleep(12.5)

        # Actually grabs can
        servo.degrees_180()
        time.sleep(0.5)

        # Pulls can up
        client.send('crane run_to_rel_pos(1850)')
        time.sleep(8)

        # Reverses the robot
        client.send('reverse_short')
        time.sleep(2.5)

        # Turn clockwise until it finds the platform
        # based on timing :\
        if end_turn_time-start_turn_time < 1:
            extended_zone_time_wait = 2
        elif end_turn_time-start_turn_time < 2:
            extended_zone_time_wait = 1.5
        else:
            extended_zone_time_wait = 1.25

        extended_zone_turn_time = extended_zone_time_wait*(end_turn_time-start_turn_time)# no idea why its 2*

        rotate_time = 5.15-(end_turn_time-start_turn_time)

        if 'left' in CAN_RELATIVE_POSITION:
            client.send('clockwise_slow')
        elif 'right' in CAN_RELATIVE_POSITION:
            client.send('clockwise_anti_slow')

        start_turn_time = time.time()

        if not EXTENDED_ZONE:
            while time.time()-start_turn_time <= rotate_time:
                pass

        elif EXTENDED_ZONE:
            while time.time()-start_turn_time <= extended_zone_turn_time:
                pass

        client.send('stop')

        # If its in an extended zone it needs to go back from where it can from
        if EXTENDED_ZONE:
            client.send('set_rps(0.75)')
            time.sleep(1.5)
            client.send('run_to_rel_pos(-1200)')
            time.sleep(6.5)

            # rerotates itself so it faces platform
            if 'left' in EXTENDED_ZONE_LOCATION:
                client.send('left run_to_rel_pos(230)')
                time.sleep(0.125)
                client.send('right run_to_rel_pos(-230)')

            elif 'right' in EXTENDED_ZONE_LOCATION:
                client.send('right run_to_rel_pos(230)')
                time.sleep(0.125)
                client.send('left run_to_rel_pos(-230)')

            time.sleep(1.5)


        # Go forward until reaches platform
        client.send('change_rps(0.35)')

        # 4 seconds should be enough
        time.sleep(4)

        if EXTENDED_ZONE:
            time.sleep(3)

        client.send('stop')

        # Reverses a little bit
        client.send('run_to_rel_pos(-100)')
        time.sleep(1)

        # Drops can
        servo.degrees_0()

        time.sleep(2)

        client.send('change_rps(-0.75)')

        # Yay finished the course!
        break

    # Does it detect a greenbox
    if pi_img_procs.get_is_greenbox():
        # Gets greenbox location
        greenbox_location = pi_img_procs.get_greenbox_location()

        while 'unknown' in greenbox_location:
            greenbox_location=pi_img_procs.get_greenbox_location()

        # Goes slowly along blackline until passes the greenbox
        while pi_img_procs.get_is_greenbox():
            pi_img_procs.update()
            client.send('right change_rps('+str(math.ceil(pi_img_procs.get_rmotor_value()/3*100)/100)+')')
            client.send('left change_rps('+str(math.ceil(pi_img_procs.get_lmotor_value()/3*100)/100)+')')

        time.sleep(0.5)
        # Starts over the blackline (if any)
        # Sleep helps provide consistent packet sending
        client.send('nudge_forward')
        time.sleep(1.5)

        # Sends robot in direction of the greenbox
        if 'left' in greenbox_location:
            client.send('clockwise_anti_slow')

        elif 'right' in greenbox_location:
            client.send('clockwise_slow')

        time.sleep(2.15)

        # This is merely a pattern formed in robocup 2015
        # that we're taking advantage of
        while pi_img_procs.get_is_black_line_straight():
            pi_img_procs.update()

        while not pi_img_procs.get_is_black_line_straight():
            pi_img_procs.update()

        green_time = time.time()

        # Follow blackline if we immediately see a greenbox
        while pi_img_procs.get_is_greenbox() or time.time() - green_time < 0.5:
            pi_img_procs.update()
            client.send('right change_rps('+str(math.ceil(pi_img_procs.get_rmotor_value()/3*   100)/100)+')')
            client.send('left change_rps('+str(math.ceil(pi_img_procs.get_lmotor_value()/3*    100)/100)+')')

    # Updates camera feed
    pi_img_procs.update()

    # Rotates motor according to camera feed
    client.send(pi_img_procs.get_rmotor_cmd())
    client.send(pi_img_procs.get_lmotor_cmd())
