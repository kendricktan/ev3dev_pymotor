#!/usr/bin/python -tt
import os
import sys
import math
import socket

# Reloads libraries
sys.path.append('/usr/local/lib/python2.7/site-packages')

import cv2
import time
import numpy as np

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

# Loads the module for pi camera
os.system('sudo modprobe bcm2835-v4l2')

# PID
PID_MULTI_THRES = 0.2718 # Value of PID total to be multiplied by

KP = 0.03
KI = 0
KD = 0
DERIVATOR = 0

P_VAL = 0
I_VAL = 0
D_VAL = 0

I_MAX = 0.25
I_MIN = 0

PID_TOTAL = 0

ERROR = 0
MOTOR_RPS = 0.2 # rotations per scond
MOTOR_RPS_MIN = 0

# If line is on the right = negative value

# COLORS ARE IN BGR
RED_COLOR = (43, 57, 192)
GREEN_COLOR = (113, 204, 46)
BLUE_COLOR = (219, 152, 52)
YELLOW_COLOR = (131, 130, 224)

# THRESHOLDS
CAMERA_WIDTH = 320
CAMERA_HEIGHT = 240
MIDDLE = CAMERA_WIDTH/2

THRESH = 100 # Change threshold to high if can't detect line; Change to lower if detects too many
AREA_THRESH = 200

ROI_DIF = 20

# END THRESHOLD

# Get pi camera stream
cap = cv2.VideoCapture(0)

# Set the resolution of the stream
cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)

# Counter for fps
counter = 0

print 'Starting line detection...'

while True:
    # Gets frame
    ret, frame = cap.read()

    # Define our regions of interest
    ROI = frame [80:120, 0:320]
    ROI2 = frame [100:140, 0:320]
    ROI3 = frame [120:160, 0:320]

    # Converts ROI into Grayscale
    im_ROI = cv2.cvtColor(ROI, cv2.COLOR_BGR2GRAY)
    im_ROI2 = cv2.cvtColor(ROI2, cv2.COLOR_BGR2GRAY)
    im_ROI3 = cv2.cvtColor(ROI3, cv2.COLOR_BGR2GRAY)

    # Apply THRESHold filter to smoothen edges and convert images to negative
    # Maybe change to otsu or gaussian threshold
    ret, im_ROI = cv2.threshold(im_ROI, THRESH, 255, 0)
    cv2.bitwise_not(im_ROI, im_ROI)

    ret, im_ROI2 = cv2.threshold(im_ROI2, THRESH, 255, 0)
    cv2.bitwise_not(im_ROI2, im_ROI2)

    ret, im_ROI3 = cv2.threshold(im_ROI3, THRESH, 255, 0)
    cv2.bitwise_not(im_ROI3, im_ROI3)

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

    # Variables to store ALL contour_coordinates
    contour_no = 0
    contour_coordinates = []

    # List to store INTERESTED contour_coordinates
    contour_coordinates_priority = []

    # Loop through each contours
    for j in contours, contours2, contours3:
        for i in j:
            # Gets the area of each contour
            area = cv2.contourArea(i)

            # Get dictionary keys for moments
            moments = cv2.moments (i)
            #cv2.putText(frame,'Area ' + str(contour_no+1) + " :" + str(area),(10,25+(ROI_DIF*contour_no)), cv2.FONT_HERSHEY_PLAIN, 1, (255,0,0),2)

            # We only want to get an area of > the threshold to prevent not usable contours
            if area>AREA_THRESH: 
                if moments['m00']!=0.0:
                    if moments['m01']!=0.0:
                        # We can calculate the centroid coordinates using this
                        cx = int(moments['m10']/moments['m00'])         # cx = M10/M00
                        cy = int(moments['m01']/moments['m00'])         # cy = M01/M00

                        # Draw inner circle
                        #cv2.circle(frame,(cx,cy+80+(ROI_DIF*contour_no)), 4, BLUE_COLOR, -1)

                        # Draw outer circle
                        #cv2.circle(frame,(cx,cy+80+(ROI_DIF*contour_no)), 8, GREEN_COLOR, 0)

                        # Draw rectangle
                        #x,y,w,h = cv2.boundingRect(i)
                        #cv2.rectangle(frame,(x,y+80+(ROI_DIF*contour_no)),(x+w,y+h+80+(ROI_DIF*contour_no)),(0,255,0),2)

                        # Store our centroid coordinates                        
                        contour_coordinates.append((cx, cy+80+(ROI_DIF*contour_no)))

                        # Find contours which are closest to the middle (so PID can be performed)
                        if len(contour_coordinates_priority) >= (contour_no+1):
                            if abs(MIDDLE-cx) <= abs(MIDDLE-contour_coordinates_priority[contour_no][0]):
                                contour_coordinates_priority[contour_no] = (cx, cy)
                            
                        else:
                            contour_coordinates_priority.append((cx, cy+80+(ROI_DIF*contour_no)))
    
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
        
        #I_VAL = I_VAL + ERROR
        
        if I_VAL > I_MAX:
            I_VAL = I_MAX
        elif I_VAL < I_MIN:
            I_VAL = I_MIN
        
        PID_VAL = P_VAL + D_VAL + I_VAL
        
        PID_TOTAL += (PID_MULTI_THRES/(i+1))*PID_VAL
        
        #cv2.putText(frame, str(i) + ' PID: ' + str(PID_VAL), (CAMERA_WIDTH/2,160+(i*20)), cv2.FONT_HERSHEY_PLAIN, 1, YELLOW_COLOR,2)
        i = i + 1
        
    #cv2.putText(frame, 'PID: ' + str(PID_TOTAL), ((CAMERA_WIDTH)/2, 160), cv2.FONT_HERSHEY_PLAIN, 1, YELLOW_COLOR, 2)

    # Sends signal to ev3
    R_MOTOR_RPS = MOTOR_RPS+PID_TOTAL
    L_MOTOR_RPS = MOTOR_RPS-PID_TOTAL

    R_MOTOR_RPS = MOTOR_RPS_MIN if R_MOTOR_RPS < MOTOR_RPS_MIN else R_MOTOR_RPS
    L_MOTOR_RPS = MOTOR_RPS_MIN if L_MOTOR_RPS < MOTOR_RPS_MIN else L_MOTOR_RPS
    
    client.send('right change_rps(' + str(R_MOTOR_RPS) + ')')
    print 'right change_rps(' + str(R_MOTOR_RPS) + ')'

    client.send('left change_rps(' + str(L_MOTOR_RPS) + ')')
    print 'left change_rps(' + str(L_MOTOR_RPS) + ')'

    
    # Overflow protection
    if counter >= sys.maxint - 100000:
        counter = 0
    
    # Draw connecting lines
    #if len(contour_no) >= 3:
        #cv2.line(frame, (contour_coordinates[0]), (contour_coordinates[1]), RED_COLOR, 2)
        #cv2.line(frame, (contour_coordinates[1]), (contour_coordinates[2]), RED_COLOR, 2)q

    # Display GUI for captured frame
    #if frame is not None:
        #cv2.imshow('pi camera', frame)        

    # Debug
    #if cv2.waitKey(1) & 0xFF == ord('d'):
        #print contour_coordinates

    # Wait for key press
    #if cv2.waitKey(1) & 0xFF == ord('q'):
        #break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

