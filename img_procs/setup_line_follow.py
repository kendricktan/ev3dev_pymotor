#!/usr/bin/python -tt
import os, sys

# Add cv2 library path
sys.path.append('/usr/local/lib/python2.7/site-packages')
# Loads the module for pi camera
os.system('sudo modprobe bcm2835-v4l2')

import math
import socket
import cv2
import time
import numpy as np
from settings import *

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

print 'Successfully connected to ' + TCP_IP +  '...'

# Get pi camera stream
cap = cv2.VideoCapture(0)

# Set the resolution of the stream
cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)

print 'Started webcam...'

# Counter to prevent overflow
counter = 0

while True:
    # Gets frame
    ret, frame = cap.read()

    # Define our regions of interest
    ROI = frame [ROI_Y:(ROI_Y+40), 0:320]
    ROI2 = frame [ROI2_Y:(ROI2_Y+40), 0:320]
    ROI3 = frame [ROI3_Y:(ROI3_Y+40), 0:320]
    ROIg = frame [ROIg_Y:(ROIg_Y+40), 0:320]

    # Green filter
    for (lower, upper) in GREEN_RANGE:
        # Create numpy arrays from boundaries
        lower = np.array(lower, dtype='uint8')
        upper = np.array(upper, dtype='uint8')

        # Find the colors within the specific boundary and apply the mask
        mask = cv2.inRange(ROIg, lower, upper)
        ROIg = cv2.bitwise_and(ROIg, ROIg, mask=mask)  
        
    # Converts ROI into Grayscale
    im_ROI = cv2.cvtColor(ROI, cv2.COLOR_BGR2GRAY)
    im_ROI2 = cv2.cvtColor(ROI2, cv2.COLOR_BGR2GRAY)
    im_ROI3 = cv2.cvtColor(ROI3, cv2.COLOR_BGR2GRAY)     
    im_ROIg = cv2.cvtColor(ROIg, cv2.COLOR_BGR2GRAY)
    
    # Apply THRESHold filter to smoothen edges and convert images to negative
    ret, im_ROI = cv2.threshold(im_ROI, THRESH, 255, 0)
    cv2.bitwise_not(im_ROI, im_ROI)

    ret, im_ROI2 = cv2.threshold(im_ROI2, THRESH, 255, 0)
    cv2.bitwise_not(im_ROI2, im_ROI2)

    ret, im_ROI3 = cv2.threshold(im_ROI3, THRESH, 255, 0)
    cv2.bitwise_not(im_ROI3, im_ROI3)

    ret, im_ROIg = cv2.threshold(im_ROIg, THRESH, 255, 0)
    # Do NOT bitwise_not im_ROIg
    
    # Reduces noise in image and dilate to increase white region (since its negative)
    erode_e = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3));
    dilate_e = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5));

    cv2.erode(im_ROI, erode_e)
    cv2.dilate(im_ROI, dilate_e)

    cv2.erode(im_ROI2, erode_e)
    cv2.dilate(im_ROI2, dilate_e)

    cv2.erode(im_ROI3, erode_e)
    cv2.dilate(im_ROI3, dilate_e)

    # Find contours
    contours, hierarchy = cv2.findContours(im_ROI,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    contours2, hierarchy = cv2.findContours(im_ROI2,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    contours3, hierarchy = cv2.findContours(im_ROI3,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    contoursg, hierarchy = cv2.findContours(im_ROIg,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    # Variables to store ALL contour_coordinates
    contour_no = 0
    contour_coordinates = []

    # List to store INTERESTED contour_coordinates
    contour_coordinates_priority = []

    # Loop through each contours
    for j in contours, contours2, contours3, contoursg:
        for i in j:
            # Gets the area of each contour
            area = cv2.contourArea(i)

            # Get dictionary keys for moments
            moments = cv2.moments (i)

            # We only want to get an area of > the threshold to prevent not usable contours
            if area>AREA_THRESH:
                if moments['m00']!=0.0:
                    if moments['m01']!=0.0:
                        # We can calculate the centroid coordinates using this
                        cx = int(moments['m10']/moments['m00'])         # cx = M10/M00
                        cy = int(moments['m01']/moments['m00'])         # cy = M01/M00

                        # Store our centroid coordinates
                        contour_coordinates.append((cx, cy))

                        # Find contours which are closest to the middle (so PID can be performed)
                        if len(contour_coordinates_priority) >= (contour_no+1):
                            if abs(MIDDLE-cx) <= abs(MIDDLE-contour_coordinates_priority[contour_no][0]):
                                contour_coordinates_priority[contour_no] = (cx, cy)

                        else:
                            contour_coordinates_priority.append((cx, cy))

        # Variable to notify us which contour we're on (contours, contours2, or contours3)
    	contour_no += 1

    # Draw interested contour coordinates
    i = 0
    PID_TOTAL = 0
    for c in contour_coordinates_priority:
        # Update PID code here
        ERROR = MIDDLE-c[0] # Gets error between target value and actual value
        P_VAL = KP*ERROR # Gets proportional val
        D_VAL = KD*(ERROR-DERIVATOR) # Gets derivative val
        DERIVATOR = ERROR

        I_VAL = I_VAL + ERROR

        if I_VAL > I_MAX:
            I_VAL = I_MAX
        elif I_VAL < I_MIN:
            I_VAL = I_MIN

        PID_VAL = P_VAL + D_VAL + I_VAL

        # Strength of each PID is determined by its placing (Furthest = more, nearest = less)
        PID_TOTAL += (PID_MULTI_THRES/(i+1))*PID_VAL
        # Or PID_TOTAL += (PID_MULTI_THRES*(i+1))*PID_VAL

        i = i + 1

    # Sends signal to ev3
    R_MOTOR_RPS = MOTOR_RPS+PID_TOTAL
    L_MOTOR_RPS = MOTOR_RPS-PID_TOTAL

    R_MOTOR_RPS = MOTOR_RPS_MIN if R_MOTOR_RPS < MOTOR_RPS_MIN else R_MOTOR_RPS
    L_MOTOR_RPS = MOTOR_RPS_MIN if L_MOTOR_RPS < MOTOR_RPS_MIN else L_MOTOR_RPS

    R_MOTOR_RPS = math.ceil(R_MOTOR_RPS * 100) / 100.0
    L_MOTOR_RPS = math.ceil(L_MOTOR_RPS * 100) / 100.0

    # If it detects line(s)
    if len(contour_coordinates_priority) >= 1:
        client.send('right change_rps(' + str(R_MOTOR_RPS) + ')')
        print 'right change_rps(' + str(R_MOTOR_RPS) + ')'

        client.send('left change_rps(' + str(L_MOTOR_RPS) + ')')
        print 'left change_rps(' + str(L_MOTOR_RPS) + ')'

    # Run forever until redetects the lines
    else:
        client.send('run_forever')
        print 'run_forever'

    # Overflow protection
    if counter >= sys.maxint - 100000:
        counter = 0

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

