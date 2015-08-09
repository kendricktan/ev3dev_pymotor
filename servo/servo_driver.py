import RPi.GPIO as GPIO
import time

class servo_driver:
    def __init__(self, GPIO_port):
        # Disable warnings
        GPIO.setwarnings(False)

        # Sets GPIO to read GPIO no instead of port no
        # (e.g. GPIO 14 @ port 8 = 14)
        GPIO.setmode(GPIO.BCM)

        # GPIO port assigned is an output port
        GPIO.setup(GPIO_port, GPIO.OUT)

        # Sets up pulse width modulation for servo
        # PWM runs at 50hz or 20ms
        self.pwm = GPIO.PWM(GPIO_port, 50)

        # Starts pulse width modulation
        self.pwm.start(7.5)

    # Sets servo to 0 degrees
    def degrees_0(self):
        self.pwm.ChangeDutyCycle(2.5)

    # Sets servo to neutral position
    def neutralposition(self):
        self.pwm.ChangeDutyCycle(7.5)

    # Sets servo to 180 degrees
    def degrees_180(self):
        self.pwm.ChangeDutyCycle(12.5)

    def __del__(self):
        GPIO.cleanup()
        self.pwm.stop()

