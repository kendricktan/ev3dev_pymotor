from send import *
from recv import *
from resources import *

class udp_cli(udp_send, udp_recv):
    # Dictionary for motors
    motors = {}
    
    # Initializes udp send and recv
    def __init__(self, MULTICAST_USERNAME, MULTICAST_ADDY, MULTICAST_PORT):
        # Initializes send and recv class
        udp_send.__init__(self, MULTICAST_USERNAME, MULTICAST_ADDY, MULTICAST_PORT)
        udp_recv.__init__(self, MULTICAST_ADDY, MULTICAST_PORT)

        # Is application running
        self.__running = True
        
        # Initialize your motors here
        self.motors['left'] = ev3dev_pymotor('outA')
        self.motors['right'] = ev3dev_pymotor('outB')
        
        self.motors['left'].set_rps(0.5)
        self.motors['right'].set_rps(0.5)
        
    
    # updates chat screen
    def update_chat(self):
        while self.__running:
            # Gets and appends data from multicast
            _data = udp_recv.get_recv_data(self)                   
            
            if 'run_forever' in data:
                self.motors['left'].run_forever()
                self.motors['right'].run_forever()
                
            if 'stop' in data:
                self.motors['left'].stop()
                self.motors['right'].stop()
            
            print _data
            
            # Moves motors according to command                            

# Start's cli main loop and multi-threads additional functions
def loop_cli(cli):    
    try:
        thread.start_new_thread(cli.update_chat, ())
        
    except Exception as e:
        print e
       
    # Keeps sending data
    _data = None
    
    while _data != '/quit':
        _data = raw_input()
        cli.send_data(_data)     
