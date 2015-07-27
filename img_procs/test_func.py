from img_procs import *

# Initalizes tcp connection
# Checks for usage help
if len(sys.argv) > 1:
    if sys.argv[1] == '-h' or sys.argv[1] == '--help':
        print 'Usage: python setup_client.py [server ip]'
        sys.exit()

TCP_PORT = 5005
TCP_IP = str(sys.argv[1]) if len(sys.argv) > 1 else ''
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((TCP_IP, 5005))


# Initialize image processing class
pi_img_procs = img_procs()

while True:
    pi_img_procs.align_horizontal_line(True)
    
    client.send(pi_img_procs.get_rmotor_cmd())
    client.send(pi_img_procs.get_lmotor_cmd())
    
    time.sleep(0.01)
