# Image settings
CAMERA_WIDTH = 320
CAMERA_HEIGHT = 240

# PID
PID_MULTI_THRES = 0.275 # Determines the weight of each PID value

KP = 0.0185
KI = 0.0075
KD = 0.011
DERIVATOR = 0

P_VAL = 0
I_VAL = 0
D_VAL = 0

I_MAX = 0.01359
I_MIN = -I_MAX

PID_TOTAL = 0

ERROR = 0

# Motor speed
MOTOR_RPS = 0.75 # rotations per scond
MOTOR_RPS_MIN = -2.0
# If line is on the right = negative value

# ROI Settings
ROI_Y = 120
ROI2_Y = 150
ROI3_Y = 180 # DON'T EXCEED 200

ROI_START = ROI_Y
ROI_DIF = abs(ROI2_Y-ROI_Y)

# Black line thresholding
MIDDLE = CAMERA_WIDTH/2
THRESH = 75 # Change threshold to higher if can't detect line; Change to lower if detects too many
AREA_THRESH = 1000

# Settings for horizontal line alignment
H_MIDDLE = CAMERA_HEIGHT/2
ROIh_X = CAMERA_WIDTH/2
ROIh_HEIGHT = 15
H_ALIGN_THRES = 3 # How many coordinates can the horizontal line be off by from (CAMERA_HEIGHT-ROIh_HEIGHT)+(ROIh_HEIGHT/2)

# Green filter thresholding
ROIg_Y = 120 # or 120
ROIh_Y = ROIg_Y-40
ROIh_AREA_THRESH = 10000 # Area threshold for ROI horizontal (line above green box, usually along x-axis)
H_BLACK_LINE_THRESH = 100 # Change to higher if can't detect; lower if detects too many


GREEN_P_VAL = 0.83 # PID for green val
GREEN_RANGE = [([105, 140, 80], [135, 160, 110])] # Increase B(G)R [G] range if detects fuzzy lines, change if can't detect
GREEN_AREA_MAX = 35000 # If exceed this, robot has reached the end
GREEN_AREA_MIN = 1000 # Area of contour before officially recognizing it
GREEN_THRESH = 100#THRESH # Change to higher if can't detect line; change to lower if detects too many


# COLORS (BGR)
RED_COLOR = (43, 57, 192)
GREEN_COLOR = (113, 204, 46)
BLUE_COLOR = (219, 152, 52)
YELLOW_COLOR = (131, 130, 224)

