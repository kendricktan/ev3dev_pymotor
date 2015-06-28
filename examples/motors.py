import time
from resources import *

# Configure motor ports
motors = {}
motors['left'] = ev3dev_pymotor('outA')
motors['right'] = ev3dev_pymotor('outB')

# Set motor rotations per second
motors['left'].set_rps(0.5)
motors['right'].set_rps(0.5)

# Make motors run forever
motors['left'].run_forever()
motors['right'].run_forever()

time.sleep(3)

# Use change RPS to change rotations per second
# when motor is moving
motors['left'].change_rps(0.2)
motors['right'].change_rps(0.75)

time.sleep(3)

motors['left'].change_rps(0.75)
motors['right'].change_rps(0.2)

time.sleep(3)

# Rememver to stop!
motors['left'].stop()
motors['right'].stop()
