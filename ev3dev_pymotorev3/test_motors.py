import time
from ev3dev_pymotor import *

motor_left = ev3dev_pymotor('outA')
motor_right = ev3dev_pymotor('outB')

motor_left.set_rps(0.5)
motor_right.set_rps(0.5)

motor_left.run_forever()
motor_right.run_forever()

time.sleep(3)

motor_left.change_rps(0.2)
motor_right.change_rps(0.75)

time.sleep(3)

motor_left.change_rps(0.75)
motor_right.change_rps(0.2)

time.sleep(3)

motor_left.stop()
motor_right.stop()
