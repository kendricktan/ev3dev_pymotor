import cv, cv2
import time
import picamera
import picamera.array

x_co = 0
y_co = 0

def on_mouse(event,x,y,flag,param):
  global x_co
  global y_co
  if(event==cv.CV_EVENT_MOUSEMOVE):
    x_co=x
    y_co=y

with picamera.PiCamera() as camera:
    with picamera.array.PiRGBArray(camera) as stream:

        camera.resolution = (320, 240)
        camera.framerate = 30

        time.sleep(2)
        # Now fix the values
        camera.shutter_speed = camera.exposure_speed
        camera.exposure_mode = 'off'
        g = camera.awb_gains
        camera.awb_mode = 'off'
        camera.awb_gains = g

        while True:
            camera.capture(stream, format='bgr', use_video_port=True)

            hsv = cv2.cvtColor(stream.array, cv2.COLOR_BGR2HSV)
            cv.SetMouseCallback("camera", on_mouse, 0)
            s=cv.Get2D(cv.fromarray(hsv),y_co,x_co)

            print "H:",s[0],"      S:",s[1],"       V:",s[2]

            src= stream.array.copy()

            cv2.putText(src, str(s[0])+","+str(s[1])+","+str(s[2]), (x_co,y_co), cv2.FONT_HERSHEY_PLAIN, 1, (55,25,255), 2)
            cv2.imshow('camera', src)

            if cv.WaitKey(1) & 0xFF == ord('q'):
                break

            stream.seek(0)
            stream.truncate()

