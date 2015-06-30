import socket, sys

class client_tcp:
    MSG = ''
    TCP_IP = ''
    TCP_PORT = 5005

    def __init__(self, TCP_IP, TCP_PORT):
        # Binds and establishes a connection to the
        # specified ip address and port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((TCP_IP, TCP_PORT))

    def __init__(self, TCP_IP):
        # Binds and establishes a connection to the
        # specified ip address and port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((TCP_IP, self.TCP_PORT))

    def __init__(self):
        # Binds and establishes a connection to the
        # specified ip address and port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.TCP_IP, self.TCP_PORT))

    def client_loop(self):
        # Keeps sending commands to the server until
        # '/quit', in which both server and client terminates
        # the established connection
        while '/quit' not in self.MSG:
            self.MSG = raw_input()
            self.s.send(self.MSG)

    def __del__(self):
        # Closes connection
        self.s.close()
