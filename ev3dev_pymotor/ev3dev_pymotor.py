import glob

# Class initalize example:
# ev3dev_pymotor('outA', 'outB') <-- outA for left motor, outB for right motor

class ev3dev_pymotor:
    # Constructor
    def __init__(self, motor):
        # Set motor port
        self.motor_port = motor

        # Initializes settings
        self.init_settings()

    # Destructor
    def __del__(self):
        self.stop()

    def init_settings(self):
        # Initializes the motor numbers via the output port
        for f in glob.glob('/sys/class/tacho-motor/motor*'):
             if self.motor_port in open(f+'/port_name', 'rb').read():
                self.motor = f

        # Reset motor settings
        if self.motor is not None:
            with open(self.motor+'/command', 'w') as f:
                f.write('reset')

        # We're using speed regulation for motor control
        with open(self.motor+'/speed_regulation', 'w') as f:
            f.write('on')

        # Use brake for stopping
        with open(self.motor+'/stop_command', 'w') as f:
            f.write('brake')

    # Set rotations per second
    # 360 tacho count = 1 revolution
    def set_rps(self, rps):
        rps = float(rps)*360
        rps = str(int(rps))
        with open(self.motor+'/speed_sp', 'w') as f:
            f.write(rps)

    # Runs motor forever
    def run_forever(self):
        with open(self.motor+'/command', 'w') as f:
            f.write('run-forever')

    # Stops motor
    def stop(self):
        with open(self.motor+'/command', 'w') as f:
            f.write('stop')

    # Change motor rotations
    # Use this only if motor is already running (forever)
    def change_rps(self, rps):
        self.set_rps(rps)
        self.run_forever()

    def debug(self):
        print self.motor
