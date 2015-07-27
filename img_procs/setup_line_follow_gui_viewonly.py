from img_procs import *

# Initialize image processing class
pi_img_procs = img_procs()

# we want GUI
pi_img_procs.show_gui(True)

while True:
    pi_img_procs.update()
    time.sleep(0.01)
