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

# THRESHOLDING
MIDDLE = CAMERA_WIDTH/2

THRESH = 55 # Change threshold to high if can't detect line; Change to lower if detects too many
AREA_THRESH = 200

# Green filter
ROIg_Y = 120
GREEN_RANGE = [([0, 75, 0], [60, 125, 60])] # Increase B(G)R [G] range if detects fuzzy lines
GREEN_AREA_MAX = 35000 # If exceed this, robot has reached the end
GREEN_AREA_MIN = 250 # Area of contour before officially recognizing it

# COLORS (BGR)
RED_COLOR = (43, 57, 192)
GREEN_COLOR = (113, 204, 46)
BLUE_COLOR = (219, 152, 52)
YELLOW_COLOR = (131, 130, 224)

