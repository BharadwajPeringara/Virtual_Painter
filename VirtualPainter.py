import cv2 as cv
import numpy as np
import HandTrackingModule as htm


cap = cv.VideoCapture(0)
cap.set(3, 1300)
cap.set(4, 720)

detector = htm.handDetector(detectionCon=0.8)

while True:
    success, frame =cap.read()
    frame = cv.flip(frame,1)
    cv.rectangle(frame, (20,10), (300,100), (0,0,255), cv.FILLED)
    cv.rectangle(frame, (320,10), (640,100), (0,255,0), cv.FILLED)
    cv.rectangle(frame, (650,10), (950,100), (255,0,0), cv.FILLED)
    cv.rectangle(frame, (970,10), (1280,100), (0,0,0))
    cv.putText(frame, 'Erase', (1080,60), cv.FONT_HERSHEY_COMPLEX, 1, (0,0,0), 2)

    #1. find hand landmarks

    frame = detector.findHands(frame)
    imlist = detector.findPosition(frame, draw=False)
    if len(imlist) != 0:
        # print(imlist)
        
        x1,y1 = imlist[8][1:]
        x2,y2 = imlist[12][1:]
        print(x1,y1)
    #2 find which finger is up
    #3 selection mode - two finger is up
    #4 drawing mode - one is up (index finger)

    cv.imshow('camera', frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
    
