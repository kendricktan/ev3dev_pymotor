from resources import *

sensor01 = us_read(14, 15) #Sensor is attached GPIO ports 14 and 15

print sensor01.read()
