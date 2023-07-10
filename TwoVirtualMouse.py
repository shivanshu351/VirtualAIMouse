import cv2 as cv
import mediapipe as mp
import HandTrackingModule as htm
import time
import math
import pyautogui as pag
import mediapipe as mp

#list to store the handlms
lmlist=[]
#screen_width,screen_height
screen_width,screen_height=pag.size()
#find postion function to return the array of landmarks x and y points
def Findposition(frame, handNo=0, draw=True):
    lmList = []
    if results.multi_hand_landmarks:
        myHand = results.multi_hand_landmarks[handNo]
        for id, lm in enumerate(myHand.landmark):
            # print(id, lm)
            h, w, c = frame.shape
            cx, cy = int(lm.x * w), int(lm.y * h)
            # print(id, cx, cy)
            lmList.append([id, cx, cy])
    return lmList
#capturing Video Frame by frame
cap=cv.VideoCapture(1)

mphands=mp.solutions.hands
hands=mphands.Hands()
mpDraw=mp.solutions.drawing_utils
while(True):
    isTrue,frame=cap.read()
    frameRgb=cv.cvtColor(frame,cv.COLOR_BGR2RGB)
    results=hands.process(frame)
    lmList = Findposition(frame, draw=False)
    cv.flip(frame,1)
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(frame,handLms,mphands.HAND_CONNECTIONS)

    if len(lmList) != 0:
        w,h,c=frame.shape
        #moving cursor using the middleFinger finger
        x1, y1 = lmList[12][1], lmList[12][2]
        cv.circle(frame, (x1, y1), 10, (255, 0, 0), cv.FILLED)
        index_x,index_y=screen_width/w*x1,screen_height/h*y1
        pag.moveTo(index_x,index_y)
        x2, y2 = lmList[8][1], lmList[8][2]
        index_x, index_y = screen_width / w * x2, screen_height / h * y2
        cv.circle(frame, (x2, y2), 10, (255, 0, 0), cv.FILLED)
        cv.line(frame, (x1, y1), (x2, y2), (255, 0, 0), 3)
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        cv.circle(frame, (cx, cy), 10, (255, 0, 0), cv.FILLED)
        length = math.hypot(x2 - x1, y2 - y1)  # length of the line between 12 and 8
        print(length)
        if length<40:
            pag.click()
            pag.sleep(1)
    if cv.waitKey(10)==ord('q'):
        break

    cv.imshow('video',frame)
cap.release()
cv.destroyAllWindows()