import cv2 as cv
import numpy as np
import HandTrackingModule as htm
import time

cap=cv.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

drawColor =(0,0,0)
brushsize=20
erasersize=50

pTime=0

imgcanvas=np.zeros((720,1280,3),np.uint8)


detector=htm.handDetector(detectionCon=0.8)

while True:
    success,frame=cap.read()
    frame=cv.flip(frame,1)

    cv.rectangle(frame,(20,10),(300,100),(0,0,255),cv.FILLED)
    cv.rectangle(frame,(310,10),(640,100),(0,255,0),cv.FILLED)
    cv.rectangle(frame,(650,10),(950,100),(255,0,0),cv.FILLED)
    cv.rectangle(frame,(960,10),(1280,100),(0,0,0))
    cv.putText(frame,'Eraser',(1050,70),cv.FONT_HERSHEY_COMPLEX,1,(0,0,0),3)
    


#1.find hand landmarks

    frame=detector.findHands(frame)
    imlist=detector.findPosition(frame,draw=False)
   
    if len(imlist)!=0:
        # print(imlist)

        x1,y1=imlist[8][1:]
        x2,y2=imlist[12][1:]
        # print("index finger :", x1,y1)
        # print("middle finger :",x2,y2 )
#2.find which finger is up



        fingers=detector.fingersUp()
        # print(fingers)
    

#3.selction mode - two finger is up

        if fingers[1] and fingers[2]:
            print("selection mode")

            xp,yp=0,0

            if y1<100:
                if 20<x1<300:
                    drawColor=(0,0,255)

                elif 310<x1<640:
                    drawColor=(0,255,0)
                elif 650<x1<950:
                    drawColor=(255,0,0)
                elif 960<x1<1280:
                    drawColor=(0,0,0)



                

            cv.circle(frame,(x2,y2),20,drawColor,cv.FILLED)



#4.drawing mode - one is up( index finger )

        if fingers[1] and fingers[2]==False:
            print("drawing mode")

            if xp==0 and yp==0:
                xp,yp=x1,y1

            xp,yp=x1,y1

            if drawColor==(0,0,0):
                cv.line(frame,(xp,yp),(x1,y1),drawColor,erasersize)
                cv.line(imgcanvas,(xp,yp),(x1,y1),drawColor,erasersize)


            else:



                cv.line(frame,(xp,yp),(x1,y1),drawColor,brushsize)
                cv.line(imgcanvas,(xp,yp),(x1,y1),drawColor,brushsize)






            cv.circle(frame,(x1,y1),20,drawColor,cv.FILLED)


    imggray= cv.cvtColor(imgcanvas,cv.COLOR_BGR2GRAY)
    _,imginv=cv.threshold(imggray,50,255,cv.THRESH_BINARY_INV)
    imginv=cv.cvtColor(imginv,cv.COLOR_GRAY2BGR)
    frame=cv.bitwise_and(frame,imginv)
    frame=cv.bitwise_or(frame,imgcanvas)

    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime

    cv.putText(frame,str(int(fps)),(50,200),cv.FONT_HERSHEY_COMPLEX,5,(0,255,255),5)


    frame=cv.addWeighted(frame,1,imgcanvas,0.5,0)



    # cv.imshow('canvas', imgCanvas)
    cv.imshow('camera', frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
    
