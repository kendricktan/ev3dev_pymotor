from settings import *
import time

# Format: [left|right] [command (i.e run_forever, change_rps(0.5)...]
def translate(raw_str):
    _str = raw_str.split()

    if len(_str) == 0:
        return

    # If not specify which motor
    # automatically assumes all motors
    # in list
    # Special functions will also be translated here

    # Also we only wanna move left and right motors
    # We don't wanna move crane unless specifically specified
    if len(_str) <= 1:
        if 'run_forever' in _str[0]:
    	    try:
                for motor in motors:
                    if 'crane' not in motor:
                        motors[motor].run_forever()
            except:
                pass

        elif 'stop' in _str[0]:
            try:
                for motor in motors:
                    if 'crane' not in motor:
                        motors[motor].stop()
            except:
                pass

        elif 'toggle' in _str[0]:
            try:
                for motor in motors:
                    if 'crane' not in motor:
                        motors[motor].toggle()
            except:
                pass

        elif 'set_rps' in _str[0]:
            try:
                args = _str[0][_str[0].find('(')+1:_str[0].find(')')]
                for motor in motors:
                    if 'crane' not in motor:
                        motors[motor].set_rps(float(args))
            except:
                pass

        elif 'change_rps' in _str[0]:
            try:
                args = _str[0][_str[0].find('(')+1:_str[0].find(')')]
                for motor in motors:
                    if 'crane' not in motor:
                        motors[motor].change_rps(float(args))
            except:
                pass

        elif 'run_to_rel_pos' in _str[0]:
            try:
                args = _str[0][_str[0].find('(')+1:_str[0].find(')')]
                for motor in motors:
                    if 'crane' not in motor:
                        motors[motor].run_to_rel_pos(int(args))
            except:
                pass

        ### Special commands ###

        # Turns 90 degrees anti clockwise
        elif 'anticlockwise_90' in _str[0]:
            try:
                for motor in motors:
                    motors[motor].set_rps(0.75)

                    # Assuming motor has 'left' motor
                    if 'left' in motor:
                        motors[motor].run_to_rel_pos(-MOTOR_ROTATION_TO_90_DEGREES)
                    elif 'right' in motor:
                        motors[motor].run_to_rel_pos(MOTOR_ROTATION_TO_90_DEGREES)

                # Allows motors to finish executing command before continuing
                time.sleep(1.85)

            except:
                pass

        # Turns 90 degrees clockwise
        elif 'clockwise_90' in _str[0]:
            try:
                for motor in motors:
                    motors[motor].set_rps(0.75)

                    if 'left' in motor:
                        motors[motor].run_to_rel_pos(MOTOR_ROTATION_TO_90_DEGREES)
                    elif 'right' in motor:
                        motors[motor].run_to_rel_pos(-MOTOR_ROTATION_TO_90_DEGREES)

                time.sleep(1.85)

            except:
                pass

        # Nuges forward just a bit
        elif 'nudge_forward' in _str[0]:
            try:
                for motor in motors:
                    motors[motor].stop()
                    motors[motor].set_rps(0.75)

                time.sleep(0.075)

                for motor in motors:
                    motors[motor].run_to_rel_pos(145)

                time.sleep(1)

            except:
                pass

        # Command to move towards green blocks
        elif 'green_at_right' in _str[0]:
            try:
                # Stops motor and sets RPS
                for motor in motors:
                    motors[motor].stop()
                    motors[motor].set_rps(0.75)

                time.sleep(0.25)

                # Move just slightly up
                for motor in motors:
                    if 'left' in motor:
                        motors[motor].run_to_rel_pos(MOTOR_GREEN_FORWARD)

                    elif 'right' in motor:
                        motors[motor].run_to_rel_pos(MOTOR_GREEN_FORWARD)

                time.sleep(1.25)

                # Rotate 45 degrees clockwise
                '''
                for motor in motors:
                    if 'left' in motor:
                        motors[motor].run_to_rel_pos(MOTOR_ROTATION_GREEN)
                    elif 'right' in motor:
                        motors[motor].run_to_rel_pos(-MOTOR_ROTATION_GREEN)

                time.sleep(0.65)
                '''

                # Stop and set rps
                for motor in motors:
                    motors[motor].stop()

                    if 'left' in motor:
                        motors[motor].set_rps(0.25)
                    elif 'right' in motor:
                        motors[motor].set_rps(-0.25)

            except:
                pass

        elif 'green_at_left' in _str[0]:
            try:
                # Stops motor and sets RPS
                for motor in motors:
                    motors[motor].stop()
                    motors[motor].set_rps(0.75)

                time.sleep(0.25)

                # Move just slightly up
                for motor in motors:
                    if 'left' in motor:
                        motors[motor].run_to_rel_pos(220)

                    elif 'right' in motor:
                        motors[motor].run_to_rel_pos(220)

                time.sleep(1.25)

                # Rotate 45 degrees anticlockwise
                '''
                for motor in motors:
                    if 'left' in motor:
                        motors[motor].run_to_rel_pos(-MOTOR_GREEN_FORWARD)
                    elif 'right' in motor:
                        motors[motor].run_to_rel_pos(MOTOR_GREEN_FORWARD)
                '''

                time.sleep(0.65)

                # Stop and set low rps
                for motor in motors:
                    motors[motor].stop()

                    if 'left' in motor:
                        motors[motor].set_rps(-0.25)
                    elif 'right' in motor:
                        motors[motor].set_rps(0.25)

            except:
                pass

        ### Commands for crane operation ###
        elif 'reverse_short' in _str[0]:
            try:
                motors['right'].run_to_rel_pos(-210)
                motors['left'].run_to_rel_pos(-210)

                time.sleep(2.5)

            except:
                pass

        # Nudge crane to the right for a little bit
        elif 'crane_nudge_right' in _str[0]:
            try:
                for motor in motors:
                    motors[motor].set_rps(0.75)

                motors['right'].run_to_rel_pos(-50)
                motors['left'].run_to_rel_pos(50)

                time.sleep(0.7)

            except:
                pass

        # Nude crane to the left for a little bit
        elif 'crane_nudge_left' in _str[0]:
            try:
                for motor in motors:
                    motors[motor].set_rps(0.75)

                motors['right'].run_to_rel_pos(50)
                motors['left'].run_to_rel_pos(-50)

                time.sleep(0.7)

            except:
                pass

        # Strong nudge crane to the right
        elif 'crane_s_nudge_right' in _str[0]:
            try:
                for motor in motors:
                    motors[motor].set_rps(0.75)

                motors['right'].run_to_rel_pos(-100)
                motors['left'].run_to_rel_pos(100)

                time.sleep(0.7)

            except:
                pass

        # Strong nudge crane to the left
        elif 'crane_s_nudge_left' in _str[0]:
            try:
                for motor in motors:
                    motors[motor].set_rps(0.75)

                motors['right'].run_to_rel_pos(100)
                motors['left'].run_to_rel_pos(-100)

                time.sleep(0.7)

            except:
                pass

        # Slowly turns clockwise
        elif 'clockwise_slow' in _str[0]:
            try:
                motors['left'].change_rps(0.25)
                time.sleep(0.3)
                motors['right'].change_rps(-0.25)
                time.sleep(0.3)

            except:
                pass

        # Slowly turns anticlockwise
        elif 'clockwise_anti_slow' in _str[0]:
            try:
                motors['left'].change_rps(-0.25)
                time.sleep(0.3)
                motors['right'].change_rps(0.25)
                time.sleep(0.3)

            except:
                pass

        # Rotates 180 degrees
        elif 'degrees_180' in _str[0]:
            try:
                # Sets constant speed
                for motor in motors:
                    motors[motor].set_rps(0.75)

                motors['left'].run_to_rel_pos(-490)
                time.sleep(0.1)
                motors['right'].run_to_rel_pos(490)

                time.sleep(3.5)

            except:
                pass

        # Crane grab can
        elif 'can_detected' in _str[0]:
            try:
                # Sets standard RPS for motors
                for motor in motors:
                    motors[motor].set_rps(0.75)

                # 'Push' can into position
                motors['right'].run_to_rel_pos(125)
                motors['left'].run_to_rel_pos(125)
                time.sleep(0.75)
                motors['right'].run_to_rel_pos(-100)
                motors['left'].run_to_rel_pos(-100)
                time.sleep(0.55)

                # Lower crane
                motors['crane'].run_to_rel_pos(-1250)
                time.sleep(5.5)

                # 'Nudges' crane around in case it didn't land on can
                motors['right'].run_to_rel_pos(50)
                time.sleep(0.35)
                motors['right'].run_to_rel_pos(-50)
                time.sleep(0.35)

                motors['left'].run_to_rel_pos(50)
                time.sleep(0.35)
                motors['left'].run_to_rel_pos(-50)
                time.sleep(0.35)

                # Continue lowering crane
                motors['crane'].run_to_rel_pos(-500)

                # Nudges can one final time
                motors['right'].run_to_rel_pos(50)
                time.sleep(0.35)
                motors['right'].run_to_rel_pos(-50)
                time.sleep(0.35)

                motors['left'].run_to_rel_pos(50)
                time.sleep(0.35)
                motors['left'].run_to_rel_pos(-50)
                time.sleep(0.35)


            except:
                pass


        # Phase for avoiding object detected by ultrasonic sensor
        # Assuming object is around the standard dimensions of 1.x litre bottle
        elif 'us_avoid_object' in _str[0]:
            try:
                # Needa set speed to 0.75 rps as
                # it was tested under those conditions
                # Reverses back so it doesn't hit it
                for motor in motors:
                    motors[motor].set_rps(0.75)
                    motors[motor].run_to_rel_pos(-125)

                time.sleep(0.3)

                # Rototes 90 degrees
                for motor in motors:
                    # Assuming motor has 'left' motor
                    if 'left' in motor:
                        motors[motor].run_to_rel_pos(-MOTOR_ROTATION_TO_90_DEGREES)
                    elif 'right' in motor:
                        motors[motor].run_to_rel_pos(MOTOR_ROTATION_TO_90_DEGREES)

                # Allows motors to finish executing command before continuing
                time.sleep(1.6)

                # Stops for safety and sanity check
                for motor in motors:
                    motors[motor].stop()

                time.sleep(0.5)

                # Runs motor with variable speed so robot can
                # 'circulate' object
                for motor in motors:
                    if 'left' in motor:
                        motors[motor].change_rps(OUTTER_MOTOR_AVOID_RPS)
                    elif 'right' in motor:
                        motors[motor].change_rps(INNER_MOTOR_AVOID_RPS)

                # Time needed to circulate object
                time.sleep(6.25)

                # Stops motor
                # Sanity/safety check
                for motor in motors:
                    motors[motor].stop()

                time.sleep(0.5)

                # Assuming we've reached the black line
                # Turn 90 degrees to realign with line
                for motor in motors:
                    if 'left' in motor:
                        motors[motor].run_to_rel_pos(-MOTOR_ROTATION_TO_90_DEGREES)
                    elif 'right' in motor:
                        motors[motor].run_to_rel_pos(MOTOR_ROTATION_TO_90_DEGREES)

                # Wait till command finishes executing before sleeping
                time.sleep(1.85)

                # Stops motor
                for motor in motors:
                    motors[motor].stop()

                time.sleep(0.05)

            except:
                pass


    # If specify which motor beforehand then
    # only moves that motor
    elif len(_str) > 1:

        if 'run_forever' in _str[1]:
            try:
                motors[_str[0]].run_forever()
            except:
                pass

        elif 'stop' in _str[1]:
            try:
                motors[_str[0]].stop()
            except:
                pass

        elif 'toggle' in _str[1]:
            try:
                motors[_str[0]].toggle()
            except:
                pass

        elif 'set_rps' in _str[1]:
            try:
                args = _str[1][_str[1].find('(')+1:_str[1].find(')')]
                motors[_str[0]].set_rps(float(args))
            except:
                pass

        elif 'change_rps' in _str[1]:
            try:
                args = _str[1][_str[1].find('(')+1:_str[1].find(')')]
                motors[_str[0]].change_rps(float(args))
            except:
                pass

        elif 'run_to_rel_pos' in _str[1]:
            try:
                args = _str[1][_str[1].find('(')+1:_str[1].find(')')]
                motors[_str[0]].run_to_rel_pos(int(args))
            except:
                pass
