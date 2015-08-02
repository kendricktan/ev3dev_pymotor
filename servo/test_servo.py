from servo_driver import *

# Assigns output GPIO port to be 4
servo = servo_driver(4)

# Swings servo to 180 degrees
servo.degrees_180()

time.sleep(1)

# Swings servo to 0 degrees
servo.degrees_0()

time.sleep(1)

# Swings servo to neutral position
servo.neutralposition()

time.sleep(1)
