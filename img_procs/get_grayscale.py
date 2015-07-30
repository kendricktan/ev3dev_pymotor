import cv
import time
x_co = 0
y_co = 0
def on_mouse(event,x,y,flag,param):
  global x_co
  global y_co
  if(event==cv.CV_EVENT_MOUSEMOVE):
    x_co=x
    y_co=y

cv.NamedWindow("camera", 1)
capture = cv.CaptureFromCAM(0)
font = cv.InitFont(cv.CV_FONT_HERSHEY_SIMPLEX, 0.5, 1, 0, 2, 8)
while True:
    src = cv.QueryFrame(capture)
    cv.Smooth(src, src, cv.CV_BLUR, 3)
    grayscale = cv.CreateImage(cv.GetSize(src), 8, 1)
    thr = cv.CreateImage(cv.GetSize(src), 8, 1)
    cv.CvtColor(src, grayscale, cv.CV_BGR2GRAY)
    cv.SetMouseCallback("camera",on_mouse, 0);
    s=cv.Get2D(grayscale,y_co,x_co)
    print "Grayscale:",s[0]
    cv.PutText(src,str(s[0]), (x_co,y_co),font, (55,25,255))
    cv.ShowImage("camera", src)
    if cv.WaitKey(1) & 0xFF == ord('q'):
        break
