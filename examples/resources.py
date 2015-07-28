import os, sys

# Import ev3dev_pymotor libraries
PARENT_DIR = os.path.abspath('..')
sys.path.append(os.path.join(PARENT_DIR, 'ev3dev_pymotor'))
sys.path.append(os.path.join(PARENT_DIR, 'us_read'))
sys.path.append(os.path.join(PARENT_DIR, 'tcp'))
from ev3dev_pymotor import *
