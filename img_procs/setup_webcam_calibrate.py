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

from settings import *

# boundary for green filter
GREEN_ROI = 100
GREEN_RANGE  = [([0, 75, 0], [60, 125, 60])] # Increase B(G)R [G] range if detects fuzzy lines
GREEN_THRESH = 15 # Lower if can't detect, higher if detects too many
GREEN_AREA_MAX = 80000
GREEN_AREA_MIN = 200

# Loads the module for pi camera
os.system('sudo modprobe bcm2835-v4l2')

# Get pi camera stream
cap = cv2.VideoCapture(0)

# Set the resolution of the stream
cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)

# Counter to prevent overflow
counter = 0

while True:
    # Gets frame
    ret, frame = cap.read()

    # Green region of interest
    ROI_g = frame#[GREEN_ROI:(GREEN_ROI+40), 0:320]

    # Green filter
    for (lower, upper) in GREEN_RANGE:
        # Create numpy arrays from boundaries
        lower = np.array(lower, dtype='uint8')
        upper = np.array(upper, dtype='uint8')

        # Find the colors within the specific boundary and apply the mask
        mask = cv2.inRange(ROI_g, lower, upper)
        ROI_g = cv2.bitwise_and(ROI_g, ROI_g, mask=mask)

    ROI_g = cv2.cvtColor(ROI_g, cv2.COLOR_BGR2GRAY)
    ret, ROI_g = cv2.threshold(ROI_g, THRESH, 255, 0)

    # Finds contours
    contours, hierarchy = cv2.findContours(ROI_g.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


    for i in contours:
        area = cv2.contourArea(i)
        moments = cv2.moments(i)

        # We only want to get an area of > the threshold to prevent not usable contours
        if area>AREA_THRESH:
            if moments['m00']!=0.0:
                if moments['m01']!=0.0:
                                                                                                                    # We can calculate the centroid coordinates using this
                    cx = int(moments['m10']/moments['m00'])         # cx = M10/M00
                    cy = int(moments['m01']/moments['m00'])         # cy = M01/M00

                    cv2.circle(frame, (cx, cy), 4, BLUE_COLOR, -1)

    # Overflow protection
    if counter >= sys.maxint - 100000:
        counter = 0

    # Display GUI for captured frame
    if frame is not None:
        #cv2.imshow('pi camera', frame)
        cv2.imshow('pi camera', frame)

    # Debug
    if cv2.waitKey(1) & 0xFF == ord('d'):
        print contour_coordinates

    # Wait for key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

