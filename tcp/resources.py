import os, sys

# Import ev3dev_pymotor libraries
PARENT_DIR = os.path.abspath('..')
LIB_DIR = os.path.join(PARENT_DIR, 'ev3dev_pymotor')
sys.path.append(LIB_DIR)

from ev3dev_pymotor import *
