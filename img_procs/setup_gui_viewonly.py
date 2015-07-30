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
# ROIg = 4
# Grayscale = 5
img_enum = str(sys.argv[1]) if len(sys.argv) > 1 else str(0)
pi_img_procs.show_which_img(img_enum)

while True:
    pi_img_procs.update()
    time.sleep(0.01)
