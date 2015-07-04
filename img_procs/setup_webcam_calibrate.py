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
GREEN_THRESH = 25 # Lower if can't detect, higher if detects too many
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

    # Convert to grayscale
    ROI_g = cv2.cvtColor(ROI_g, cv2.COLOR_BGR2GRAY)

    ret, ROI_g = cv2.threshold(ROI_g, 0, 255, 0)

    cv2.bitwise_not(ROI_g, ROI_g)

    # Reduces noise in image and dilate to increase white region (since its negative)
    erode_e = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3));
    dilate_e = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5));

    cv2.erode(ROI_g, erode_e)
    cv2.dilate(ROI_g, dilate_e)

    # Find contours
    ROI_g = cv2.Canny(ROI_g, 100, 200)

    contours, hierarchy = cv2.findContours(ROI_g, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    c = 0


    for i in contours:
        area = cv2.contourArea(i)
        moments = cv2.moments(i)

        if area > GREEN_AREA_MIN:
            if moments['m00'] != 0.0:
                if moments['m01'] != 0.0:
                    c = c + 1
                    cx = int(moments['m10']/moments['m00'])
                    cy = int(moments['m01']/moments['m00'])#+GREEN_ROI

                    cv2.putText(frame, 'Area: ' + str(area) + '; x: ' + str(cx) + ' y: ' + str(cy), (10, 25+(c*10)), cv2.FONT_HERSHEY_PLAIN, 1,   (255, 0, 0), 2)

                    cv2.circle(frame, (cx, cy), 8, BLUE_COLOR, -1)


    # Overflow protection
    if counter >= sys.maxint - 100000:
        counter = 0

    # Display GUI for captured frame
    if frame is not None:
        cv2.imshow('pi camera', frame)
        #cv2.imshow('pi camera', ROI_g)

    # Debug
    if cv2.waitKey(1) & 0xFF == ord('d'):
        print contour_coordinates

    # Wait for key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

