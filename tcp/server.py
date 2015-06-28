import socket

SERVER_LISTEN = True
TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 32 # For fast response

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

conn, addr = s.accept()

print 'Connection address: ', addr

data = None

while SERVER_LISTEN:
    data = conn.recv(BUFFER_SIZE)

    # Don't wanna just receive null data...
    while not data:
        data = conn.recv(BUFFER_SIZE)

    if '/quit' in data:
        print 'Received kill message...'
        SERVER_LISTEN = False

    print data

conn.close()
