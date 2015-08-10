# Image settings
CAMERA_WIDTH = 320
CAMERA_HEIGHT = 240

# PID
KP = 0.0065
KI = 0.0055
KD = 0.008
DERIVATOR = 0

P_VAL = 0
I_VAL = 0
D_VAL = 0

I_MAX = 0.01359
I_MIN = -I_MAX

PID_TOTAL = 0

ERROR = 0

# Motor speed
MOTOR_RPS = 0.65 # rotations per scond
MOTOR_RPS_MIN = -2.0
# If line is on the right = negative value

# ROI Settings
ROI_Y = 120

# Black line thresholding
MIDDLE = CAMERA_WIDTH/2
THRESH = 90 # Change threshold to higher if can't detect line; Change to lower if detects too many
AREA_THRESH = 850 # Minimum area before it's considered to be a black line

# Green filter thresholding
ROIg_Y = CAMERA_HEIGHT-60

GREEN_P_VAL = 0.83 # PID for green val
GREEN_RANGE = [([30, 165, 140], [80, 255, 215])] # HSV, use get_hsv.py to calibrate it
GREEN_RANGE_2 = [([0, 0, 0], [0, 0, 0])]
GREEN_AREA_THRESH = 400 # Area of contour before officially recognizing it
GREEN_THRESH = 5 #THRESH # Change to lower if can't detect line; change to higher if detects too many

# Used to determine if black line is straight (used for calibration after green box)
BLACKLINE_MIN_X = CAMERA_WIDTH/2-(CAMERA_WIDTH/6)
BLACKLINE_MAX_X = CAMERA_WIDTH/2+(CAMERA_WIDTH/6)

# Used to detect aluminium foil
ROIa_Y = 40 #0 till this value
ALUMINIUM_RANGE = [([3, 230, 80], [40, 255, 120])]
ALUMINIUM_AREA_THRESH = 350
ALUMINIUM_THRESH = 50 # Change to lower if can't detect line; change to higher if detects too many

# COLORS (BGR)
RED_COLOR = (43, 57, 192)
GREEN_COLOR = (113, 204, 46)
BLUE_COLOR = (219, 152, 52)
YELLOW_COLOR = (131, 130, 224)

