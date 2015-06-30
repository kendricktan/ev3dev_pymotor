from ev3dev_pymotor.ev3dev_pymotor import *
from tcp.server import *

server = server_tcp()
server.server_loop()
