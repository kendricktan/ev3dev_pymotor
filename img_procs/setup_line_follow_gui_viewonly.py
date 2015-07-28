from img_procs import *

# Initialize image processing class
pi_img_procs = img_procs()

# we want GUI
pi_img_procs.show_gui(True)

# Chooses which image to display (after filtered)
# frame = 0
# ROI = 1
# ROI2 = 2
# ROI3 = 3
# ROI4 = 4
pi_img_procs.show_which_img(2)

while True:
    pi_img_procs.update()
    time.sleep(0.01)
