from ev3dev_pymotor.ev3dev_pymotor import *
from tcp.client import *

client = client_tcp('', 5005)
client.client_loop()
