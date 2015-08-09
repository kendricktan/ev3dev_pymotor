#!/usr/bin/python

import time
import RPi.GPIO as GPIO
from settings import *

# remember to change the GPIO values below to match your sensors
# GPIO output = the pin that's connected to "Trig" on the sensor
# GPIO input = the pin that's connected to "Echo" on the sensor

class us_read:
    def __init__(self, GPIO_trig, GPIO_echo):
        # Disable warnings
        GPIO.setwarnings(False)

        # Uses the value of GPIO pins (e.g. GPIO 14 @ port 8 = 14)
        GPIO.setmode(GPIO.BCM)

        # GPIO output = trig
        # GPIO input = echo
        GPIO.setup(GPIO_trig, GPIO.OUT)
        GPIO.setup(GPIO_echo, GPIO.IN)
        GPIO.output(GPIO_trig, GPIO.LOW)

        self.GPIO_trig = GPIO_trig
        self.GPIO_echo = GPIO_echo

        time.sleep(0.05)

    def read(self):
        GPIO.output(self.GPIO_trig, True)
        time.sleep(0.00001) # waits for 10Us (sensor expects)

        GPIO.output(self.GPIO_trig, False)

        while GPIO.input(self.GPIO_echo) == 0:
            signaloff = time.time()

        while GPIO.input(self.GPIO_echo) == 1:
            signalon = time.time()

        timepassed = signalon - signaloff

        return timepassed * 17000 # in cm

