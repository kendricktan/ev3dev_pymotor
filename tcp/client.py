import socket, sys

if len(sys.argv) > 1:
    if sys.argv[1] == '-h' or sys.argv[1] == '--help':
        print 'Usage: python client.py [target ip address]'
        sys.exit()

MSG = ''
TCP_IP = str(sys.argv[1]) if len(sys.argv) > 1 else '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 32 # For fast response

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

while '/quit' not in MSG:
    MSG = raw_input()
    s.send(MSG)

s.close()
