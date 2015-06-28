import socket


TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 32
MESSAGE = ""

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

while '/quit' not in MESSAGE:
    MESSAGE = raw_input()
    s.send(MESSAGE)

s.close()
