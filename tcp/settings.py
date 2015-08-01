from resources import *

### Configuration for special functions ###
# Motor rotations to turn clockwise/anticlockwise by 90 degrees
MOTOR_ROTATION_TO_90_DEGREES = 215

# Motor RPS for avoiding object
OUTTER_MOTOR_AVOID_RPS = 0.80
INNER_MOTOR_AVOID_RPS = 0.375

# Motor relative rotation to green lines
<<<<<<< HEAD
MOTOR_ROTATION_GREEN = 215
MOTOR_GREEN_FORWARD = 225
=======
MOTOR_ROTATION_GREEN = 107
MOTOR_GREEN_FORWARD = 250
>>>>>>> 480b8932c9436a1aa3e9ff6c689a098a364f3e4e

### Motor configuration ###
motors = {}

# By default it's left or right (you can change it in translate.py)
motors['left'] = ev3dev_pymotor.ev3dev_pymotor('outA')
motors['right'] = ev3dev_pymotor.ev3dev_pymotor('outB')

motors['left'].set_rps(0.5)
motors['right'].set_rps(0.5)
