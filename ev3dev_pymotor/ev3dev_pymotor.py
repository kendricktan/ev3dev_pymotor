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
        
    # Initializes motor settings
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

    # Setters
    
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
        
    # Runs motor to relative position  
    def run_to_rel_pos(self, degrees):
        # Stops motors in order to avoid 
        # clashing commands
        self.stop()
        
        # Sets position_sp
        with open(self.motor+'/position_sp', 'w') as f:
            f.write(str(degrees))
            
        # Executes command
        with open(self.motor+'/command', 'w') as f:
            f.write('run-to-rel-pos')
            

    # Toggles motor polarity and therefore direction
    def toggle(self):
        with open(self.motor+'/polarity', 'r+b') as f:
            if 'normal' in f.read():
                f.write('inversed')

            else:
                f.write('normal')

            self.run_forever()

    
    # Getters
    
    # Gets current rotation per second
    def get_rps(self):
        with open(self.motor+'/speed_sp', 'r+b') as f:
            return f.read()            
    
    def debug(self):
        print self.motor
