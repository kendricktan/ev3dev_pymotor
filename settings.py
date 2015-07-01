# PID
PID_MULTI_THRES = 0.2718 # Determines the weight of each PID value

KP = 0.0095
KI = 0.00
KD = 0.00
DERIVATOR = 0

P_VAL = 0
I_VAL = 0
D_VAL = 0

I_MAX = 0.25
I_MIN = 0

PID_TOTAL = 0

ERROR = 0
MOTOR_RPS = 0.33 # rotations per scond
MOTOR_RPS_MIN = -1.0

# If line is on the right = negative value

# ROI Settings
ROI_Y = 40
ROI2_Y = 100
ROI3_Y = 160 # DON'T EXCEED 200

ROI_START = 20
ROI_DIF = 60

# THRESHOLD
CAMERA_WIDTH = 320
CAMERA_HEIGHT = 240
MIDDLE = CAMERA_WIDTH/2

THRESH = 100 # Change threshold to high if can't detect line; Change to lower if detects too many
AREA_THRESH = 200

# COLORS ARE IN BGR
RED_COLOR = (43, 57, 192)
GREEN_COLOR = (113, 204, 46)
BLUE_COLOR = (219, 152, 52)
YELLOW_COLOR = (131, 130, 224)

