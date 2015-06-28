from send import *
from recv import *
from resources import *

class udp_cli(udp_send, udp_recv):
    # chat log list
    chat_logs = []
    
    # Initializes udp send and recv
    def __init__(self, MULTICAST_USERNAME, MULTICAST_ADDY, MULTICAST_PORT):
        # Initializes send and recv class
        udp_send.__init__(self, MULTICAST_USERNAME, MULTICAST_ADDY, MULTICAST_PORT)
        udp_recv.__init__(self, MULTICAST_ADDY, MULTICAST_PORT)

        # Is application running
        self.__running = True
        
    
    # updates chat screen
    def update_chat(self):
        while self.__running:
            # Gets and appends data from multicast
            _data = udp_recv.get_recv_data(self)       
            
            # if data is none, resend handshake cause that means we just received a handshake 
            # from a new user
            if _data is not None:
                self.chat_logs.append(_data)
                
                # Clears the screen
                # os.system('clear')
                
                # Prints everything in the log
                for chat_log in self.chat_logs:
                    print chat_log
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
