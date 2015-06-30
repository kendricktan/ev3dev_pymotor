from ev3dev_pymotor.ev3dev_pymotor import *
from tcp.client import *

# Checks for usage help
if len(sys.argv) > 1:
    if sys.argv[1] == '-h' or sys.argv[1] == '--help':
        print 'Usage: python setup_client.py [server ip]'
        sys.exit()

TCP_IP = str(sys.argv[1]) if len(sys.argv) > 1 else ''

client = client_tcp(TCP_IP)
client.client_loop()
