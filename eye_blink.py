import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector
from cvzone.PlotModule import LivePlot
import simpleaudio as sa
import time 


cap = cv2.VideoCapture(0)
detector = FaceMeshDetector(maxFaces=1)
plotY = LivePlot(640, 360, [20, 50], invert=True)
 
idList = [22, 23, 24, 26, 110, 157, 158, 159, 160, 161, 130, 243]
ratioList = []
blinkCounter = 0
counter = 0
color = (255, 0, 255)
target_time = time.time() + 58
print(target_time)
while True:
 
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
 
    success, img = cap.read()
    img, faces = detector.findFaceMesh(img, draw=False)
 
    if faces:
        face = faces[0]
        for id in idList:
            cv2.circle(img, face[id], 3,color, cv2.FILLED)
 
        leftUp = face[159]
        leftDown = face[23]
        leftLeft = face[130]
        leftRight = face[243]
        lenghtVer, _ = detector.findDistance(leftUp, leftDown)
        lenghtHor, _ = detector.findDistance(leftLeft, leftRight)
 
        cv2.line(img, leftUp, leftDown, (0, 200, 0), 2)
        cv2.line(img, leftLeft, leftRight, (0, 200, 0), 2)
 
        ratio = int((lenghtVer / lenghtHor) * 100)
        ratioList.append(ratio)
        if len(ratioList) > 3:
            ratioList.pop(0)
        ratioAvg = sum(ratioList) / len(ratioList)
 
        if ratioAvg < 28 and counter == 0:
            blinkCounter += 1
            color = (0,200,0)
            counter = 1
        if counter != 0:
            counter += 1
            if counter > 10:
                
                counter = 0
                color = (255,0, 255)
 
        cvzone.putTextRect(img, f'Blink Count: {blinkCounter}', (50, 100),
                           colorR=color)
        
        
        if blinkCounter==12 and time.time() < target_time :
            #cv2.putText(img,"Wake up",(250,250),fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=1,color=(0,0,255),thickness=4, lineType=cv2.LINE_AA)
            while True :
              # fichier = sa.WaveObject.from_wave_file("C:\\Users\\DELL\\Downloads\\Alarme-de-reveil.wav")     
              # play=fichier.play()
              # play.wait_done()
                if  cv2.waitKey(10) & 0xFF == ord('k'):
                        blinkCounter =0
                        break
                   
        elif (blinkCounter>12 or time.time() >= target_time ):
            target_time=time.time() + 58
            blinkCounter =0
            
        imgPlot = plotY.update(ratioAvg, color)
        img = cv2.resize(img, (640, 360))
        #imgStack = cvzone.stackImages([img, imgPlot], 2, 1)
        
    else:
        img = cv2.resize(img, (640, 360))
        #imgStack = cvzone.stackImages([img, img], 2, 1)
 
    cv2.imshow("Image", img)
    cv2.waitKey(25)