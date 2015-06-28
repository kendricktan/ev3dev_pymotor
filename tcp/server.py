import socket
import SocketServer

# Allows reusing address
SocketServer.ThreadingTCPServer.allow_reuse_address = True

SERVER_RUNNING = True
TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 32  # For fast response

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

conn, addr = s.accept()
while SERVER_RUNNING:
    data = conn.recv(BUFFER_SIZE)
    while not data:
        data = conn.recv(BUFFER_SIZE)

    if '/quit' in data:
        SERVER_RUNNING = False

    print data

    # Add moving robocup arm here

conn.close()
