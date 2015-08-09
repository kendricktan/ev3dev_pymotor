import socket, SocketServer

from translate import *

class server_tcp:
    SERVER_RUNNING = True
    TCP_IP = ''
    TCP_PORT = 5005

    # Small buffer size for fast response
    BUFFER_SIZE = 32

    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((self.TCP_IP, self.TCP_PORT))
        self.s.listen(1)

        self.conn, self.addr = self.s.accept()

        # Allows reusing address
        SocketServer.ThreadingTCPServer.allow_reuse_address = True

        print 'Connection established with ' + str(self.addr)

    def server_loop(self):
        while self.SERVER_RUNNING:

            self.data = self.conn.recv(self.BUFFER_SIZE)

            while not self.data:
                self.data = self.conn.recv(self.BUFFER_SIZE)

            if '/quit' in self.data:
                print 'Received terminating signal... closing server now'
                self.SERVER_RUNNING = False

            # Add moving robocup arm here
            else:
                translate(self.data)
                #print self.data

    def __del__(self):
        # Close connection
        self.conn.close()
