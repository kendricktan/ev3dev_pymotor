import socket, sys

class client_tcp:
    MSG = ''
    TCP_IP = ''
    TCP_PORT = 5005

    # Class constructor
    def __init__(self, TCP_IP):
        # Binds and establishes a connection to the
        # specified ip address and port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((TCP_IP, self.TCP_PORT))

    # Sends command via prompt
    # Useful for manual testing
    def client_loop_input(self):
        # Keeps sending commands to the server until
        # '/quit', in which both server and client terminates
        # the established connection
        while '/quit' not in self.MSG:
            self.MSG = raw_input()
            self.s.send(self.MSG)

    # Loop that doesn't require prompt
    # but requires to send command via set
    # Useful for embedding motor control in
    # custom applications
    def client_loop_set(self):
        while '/quit' not in self.MSG:
            if self.MSG != '':
                self.s.send(self.MSG)
                self.MSG = ''

    # Sets message to be sent
    # Use only in conjunction with client_loop_set
    def set_msg(self, msg):
        self.MSG = msg


    def __del__(self):
        # Closes connection
        self.s.close()
