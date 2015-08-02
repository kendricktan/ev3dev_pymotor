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

class img_procs:
    def __init__(self):
        global CAMERA_WIDTH, CAMERA_HEIGHT
    
        # Get pi camera stream
        self.cap = cv2.VideoCapture(0)

        # Sets the resolution of the stream
        self.cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
        self.cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)

        # Does it show the GUI by default
        self.is_show_gui = False

        # Which img to show (if shows GUI)
        # 0 = frame, 1 = ROI, 2 = ROIg, 3 = Grayscale img
        self.img_enum = 0

        # Does it print the commands of each motor
        self.is_print_cmd = True

        # Has it previously detected a green box
        self.is_prev_green_detected = False

        # Is the black line straight
        #(Used for calibration after greenbox)
        self.is_black_line_straight = False


    # Does it show the GUI for img processing
    def show_gui(self, is_show):
        self.is_show_gui = is_show

    # Does it print the left/right motor cmd
    # after processing it
    def print_cmd(self, is_print):
        self.is_print_cmd = is_print

    # Updates video camera stream and applies PID algorithm
    # to obtain motor rotation RPS
    def update(self):
        # Define our global variables from settings.py
        global KP, KI, KD, DERIVATOR, P_VAL, I_VAL, D_VAL, I_MAX, I_MIN, PID_TOTAL, ERROR, MOTOR_RPS, MOTOR_RPS_MIN, ROI_Y, MIDDLE, THRESH, AREA_THRESH, ROIg_Y, GREEN_P_VAL, GREEN_RANGE, GREEN_THRESH, GREEN_AREA_THRESH, US_MIN_DIST, RED_COLOR, GREEN_COLOR, BLUE_COLOR, YELLOW_COLOR

        # Gets frame from capture device
        ret, frame = self.cap.read()

        # Define our regions of interest
        # Black line ROI
        ROI = frame [ROI_Y:(ROI_Y+40), 0:320]
        
        # Greenbox ROI
        ROIg = frame [ROIg_Y:(ROIg_Y+50), 0:320]

        # Convert to HSV for more accurate reading
        ROIg = cv2.cvtColor(ROIg, cv2.COLOR_BGR2HSV)

        # Green filter
        for (lower, upper) in GREEN_RANGE:
            # Create numpy arrays from boundaries
            lower = np.array(lower, dtype='uint8')
            upper = np.array(upper, dtype='uint8')

            # Find the colors within the specific boundary and apply the mask
            mask = cv2.inRange(ROIg, lower, upper)
            ROIg = cv2.bitwise_and(ROIg, ROIg, mask=mask)

        # Converts ROI's into Grayscale
        im_ROI = cv2.cvtColor(ROI, cv2.COLOR_BGR2GRAY)
        im_ROIg = cv2.cvtColor(ROIg, cv2.COLOR_BGR2GRAY)

        # Apply Threshold filter to smoothen edges and convert images to negative
        ret, im_ROI = cv2.threshold(im_ROI, THRESH, 255, 0)
        cv2.bitwise_not(im_ROI, im_ROI)

        ret, im_ROIg = cv2.threshold(im_ROIg, GREEN_THRESH, 255, 0)
        # Do NOT bitwise_not im_ROIg

        # Reduces noise in image and dilate to increase white region (since its negative)
        erode_e = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3));
        dilate_e = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5));

        cv2.erode(im_ROI, erode_e)
        cv2.dilate(im_ROI, dilate_e)

        # Find contours
        # If we wanna show the images, we want to show
        # the UNALTERED (in the process of finding contours) images
        # so we can calibrate lighting
        if self.is_show_gui:
            contours, hierarchy = cv2.findContours(im_ROI.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            contoursg, hierarchy = cv2.findContours(im_ROIg.copy() ,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

        # if we don't want to see the gui we don't do that
        # so its more effective
        elif not self.is_show_gui:
            contours, hierarchy = cv2.findContours(im_ROI,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            contoursg, hierarchy = cv2.findContours(im_ROIg,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

        # List to store INTERESTED contour_coordinates
        blackline_x_location = -1
        greenbox_x_location = -1

        # Find contours in blackline ROI
        for i in contours:
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

                        # If we are showing our GUI
                        # then we needa draw circles
                        # indicating where we found the lines
                        if self.is_show_gui:
                            cv2.circle(frame, (cx, cy+ROI_Y), 4, BLUE_COLOR, -1)
                            cv2.putText(frame, 'Area ROI_ :' + str(area),(10, 25), cv2.FONT_HERSHEY_PLAIN, 1, (255,0,0),2)

                        # If we're previously found a coordinate
                        if blackline_x_location != -1:
                            # Find contours which are closest to the middle (so PID can be performed)
                            if abs(MIDDLE-cx) <= abs(MIDDLE-blackline_x_location):
                                blackline_x_location = cx

                        else:
                            blackline_x_location = cx       

        # Resets greenbox location
        self.is_prev_green_detected = False

        # Green contour finder in green ROI
        for i in contoursg:
            area = cv2.contourArea(i)
            moments = cv2.moments(i)

            if area > GREEN_AREA_THRESH:
                if moments['m00'] != 0.0:
                    if moments['m01'] != 0.0:
                        cx = int(moments['m10']/moments['m00'])
                        cy = int(moments['m01']/moments['m00'])

                        # If we're showing our GUI
                        # needa indicate where we found
                        # the green box
                        if self.is_show_gui:
                            cv2.circle(frame, (cx, cy+ROIg_Y), 4, GREEN_COLOR, -1)
                            cv2.putText(frame,'Area ROIg :' + str(area),(10, 170), cv2.FONT_HERSHEY_PLAIN, 1, (0,255,0),2)

                        # If we have previously found a green region
                        if greenbox_x_location != -1:
                            # Since green is indicative of where we wanna travel,
                            # we'll calculate the PID from the contour
                            # furthest away from center
                            if abs(MIDDLE-cx) >= abs(MIDDLE-greenbox_x_location):
                                # We only care about the x coordinates
                                greenbox_x_location = cx

                        else:
                            greenbox_x_location = cx

                        # We have detected a green box
                        self.is_prev_green_detected = True
                        
        # Sets is blackline straight boolean var
        # Used for calibration AFTER green box
        if blackline_x_location != -1:
            self.is_black_line_straight = True
            if blackline_x_location < BLACKLINE_MIN_X or blackline_x_location > BLACKLINE_MAX_X:
                self.is_black_line_straight = False
        else:
            self.is_black_line_straight = False

        if self.is_show_gui:
            if self.is_black_line_straight:
                cv2.putText(frame, 'Straight line detected!', (10, 210), cv2.FONT_HERSHEY_PLAIN, 1, (131, 130, 224), 2)

        # PID code
        i = 0
        PID_TOTAL = 0

        # PID calculation for motor power output
        # in order to follow line
        ERROR = MIDDLE-blackline_x_location # Gets error between target value and actual value
        P_VAL = KP*ERROR # Gets proportional val
        D_VAL = KD*(ERROR-DERIVATOR) # Gets derivative val
        DERIVATOR = ERROR

        # Calculate integral of error
        I_VAL = I_VAL + ERROR

        if I_VAL > I_MAX:
            I_VAL = I_MAX
        elif I_VAL < I_MIN:
            I_VAL = I_MIN

        #  Calculate total PID value here
        PID_VAL = P_VAL + D_VAL + I_VAL
        
        PID_TOTAL += PID_VAL

        # Calculate motor rotation per second
        R_MOTOR_RPS = MOTOR_RPS+PID_TOTAL
        L_MOTOR_RPS = MOTOR_RPS-PID_TOTAL

        R_MOTOR_RPS = MOTOR_RPS_MIN if R_MOTOR_RPS < MOTOR_RPS_MIN else R_MOTOR_RPS
        L_MOTOR_RPS = MOTOR_RPS_MIN if L_MOTOR_RPS < MOTOR_RPS_MIN else L_MOTOR_RPS

        # Only want 2 decimal places
        self.rmotor_value = R_MOTOR_RPS = math.ceil(R_MOTOR_RPS * 100) / 100.0
        self.lmotor_value = L_MOTOR_RPS = math.ceil(L_MOTOR_RPS * 100) / 100.0

        # If it detects line(s) [green or black]
        if blackline_x_location != -1:
            # Saves right motor command
            self.rmotor_cmd = 'right change_rps(' + str(R_MOTOR_RPS) + ')'
            if not self.is_show_gui:
                if self.is_print_cmd:
                    print 'right change_rps(' + str(R_MOTOR_RPS) + ')'

            # Saves left motor command
            self.lmotor_cmd = 'left change_rps(' + str(L_MOTOR_RPS) + ')'
            if not self.is_show_gui:
                if self.is_print_cmd:
                    print 'left change_rps(' + str(L_MOTOR_RPS) + ')'

        # Run forever until redetects the lines
        else:
            self.rmotor_cmd = 'right run_forever'
            self.lmotor_cmd = 'left run_forever'
            if not self.is_show_gui:
                if self.is_print_cmd:
                    print 'run_forever'

        # If we wanna see gui
        if self.is_show_gui:
            if frame is not None:
                # Show unaltered frame
                if self.img_enum == '0':
                    cv2.imshow('pi camera', frame)

                # Show specific region for blackline detection
                elif self.img_enum == '1':
                    cv2.imshow('pi camera', im_ROI)

                # Show green line detection    
                elif self.img_enum == '2':
                    cv2.imshow('pi camera', im_ROIg)

                # Show grayscale image
                elif self.img_enum == '3':
                    cv2.imshow('pi camera', cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))
                
                # B&W for whole frame    
                elif self.img_enum == '4':
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    ret, frame = cv2.threshold(frame, THRESH, 255, 0)
                    cv2.bitwise_not(im_ROI, im_ROI)
                    cv2.erode(frame, erode_e)
                    cv2.dilate(frame, dilate_e)
                    cv2.imshow('pi camera', frame)
                    

            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.__del__()

    def show_which_img(self, enum_var):
        self.img_enum = enum_var

    # Reset PID value to prevent random movement
    def reset_PID(self):
        global ERROR, P_VAL, D_VAL, DERIVATOR, I_VAL
        ERROR = 0
        P_VAL = 0
        D_VAL = 0
        DERIVATOR = 0
        I_VAL = 0

    # Calibration for green box
    # Confirmation that we've reached the end of a green box
    def get_is_greenbox(self):
        return self.is_prev_green_detected

    def reset_greenbox(self):
        self.is_prev_green_detected = False

    def get_greenbox_location(self):
        # Gets global variables from settings.py
        global GREEN_RANGE, GREEN_THRESH, MIDDLE, GREEN_AREA_THRESH

        # Gets feed from camera
        ret, frame = self.cap.read()

        # Convert to HSV for more accurate reading
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Green filter
        for (lower, upper) in GREEN_RANGE:
            # Create numpy arrays from boundaries
            lower = np.array(lower, dtype='uint8')
            upper = np.array(upper, dtype='uint8')

            # Find the colors within the specific boundary and apply mask
            mask = cv2.inRange(frame, lower, upper)
            frame = cv2.bitwise_and(frame, frame, mask=mask)

        # Converts ROI into grayscale
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Apply threshold filter to smoothen edges and convert images to negative
        ret, frame = cv2.threshold(frame, GREEN_THRESH, 255, 0)

        # Find contours
        contours, hierarchy = cv2.findContours(frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Finds out if greenbox is left or right
        right = 0
        left = 0

        for i in contours:
            area = cv2.contourArea(i)

            moments = cv2.moments(i)

            if area > GREEN_AREA_THRESH:
                if moments['m00'] != 0.0:
                    if moments['m01'] != 0.0:
                        cx = int(moments['m10']/moments['m00'])
                        cy = int(moments['m01']/moments['m00'])

                        if cx > MIDDLE:
                            right = right + 1
                        else:
                            left = left + 1

        if right > left:
            return 'right'
        elif left > right:
            return 'left'

        return 'unknown'

    def get_is_black_line_straight(self):
        return self.is_black_line_straight

    def get_rmotor_value(self):
        return self.rmotor_value

    def get_lmotor_value(self):
        return self.lmotor_value

    def get_rmotor_cmd(self):
        return self.rmotor_cmd

    def get_lmotor_cmd(self):
        return self.lmotor_cmd

    def __del__(self):
        self.cap.release()
        cv2.destroyAllWindows()

