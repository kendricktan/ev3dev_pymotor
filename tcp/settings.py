from resources import *

### Motor configuration ###
motors = {}

# By default it's left or right (you can change it in translate.py)
motors['left'] = ev3dev_pymotor('outA')
motors['right'] = ev3dev_pymotor('outB')

motors['left'].set_rps(0.5)
motors['right'].set_rps(0.5)
