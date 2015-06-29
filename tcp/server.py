import socket
import SocketServer

from translate import *

### Communication with client ###
# Allows reusing address
SocketServer.ThreadingTCPServer.allow_reuse_address = True

SERVER_RUNNING = True
TCP_IP = ''
TCP_PORT = 5005
BUFFER_SIZE = 32  # For fast response

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

conn, addr = s.accept()

print 'Connection established with ' + str(addr)

while SERVER_RUNNING:
    data = conn.recv(BUFFER_SIZE)
    while not data:
        data = conn.recv(BUFFER_SIZE)

    if '/quit' in data:
        SERVER_RUNNING = False

    # Add moving robocup arm here
    else:
        translate(data)

    #print data

# Close connection
conn.close()
