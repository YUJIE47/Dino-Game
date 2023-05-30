import cv2
import HandTrackingModule as HandTracker
import HandDetectController
import DinoPlayer1
import DinoPlayer2
import DinoBG
from pygame import time
import time as Ttime
from cvzone.HandTrackingModule import HandDetector
import sort
import numpy as np
from skimage import io
from sklearn.metrics.pairwise import cosine_similarity
import tracking
import start
import predict_module

import Mode

import SingleDinoGameControl
import SingleHandDetectControl
import SingleHandTrackModule
import SingleTracking

FPS = 30

def getPredict( hand, img ):
    x, y, w, h = hand['bbox']
    x_offset = int(w/5) # x offset
    y_offset = int(h/5)  # y offset
    x_start, x_end, y_start, y_end = x-x_offset, x+w+x_offset, y-y_offset, y+h+y_offset
    
    width = x_end - x_start
    high = y_end - y_start
    if width > high:
        temp = (width - high) // 2
        y_end = y_end + temp
        y_start = y_start - temp
    else:
        temp = (high - width) // 2
        x_end = x_end + temp
        x_start = x_start - temp
    
    pic = img[y_start:y_end, x_start:x_end]

    if ( x_start > 0 ) and (  x_end < 630 ) and ( y_start > 0 ) and ( y_end < 512 ):
        predict_hand = predict_module.Is_Particular_Gesture( pic )

    else:
        predict_hand = -1
        
    return predict_hand

def single():
    cap = cv2.VideoCapture(0)

    detector = HandDetector(mode=False, # 靜態圖模式，若爲True，每一幀都會調用檢測方法，導致檢測很慢
                        maxHands=4, # 最多檢測幾隻手
                        detectionCon=0.8, # 最小檢測置信度
                        minTrackCon=0.5)  # 最小跟蹤置信度
    gestureController = SingleHandDetectControl.GestureController()

    run = True
    DinoGame = SingleDinoGameControl.DinoGame()
    clock = time.Clock()
    mot_tracker = sort.Sort() #create instance of the SORT tracker
    id1 = 0
    coor1 = []
    hand1 = {}

    while run:
        predict_hand = 0
        # Get Input
        clock.tick(FPS)

        run = DinoGame.IsExist()
        success, img = cap.read()

        img = cv2.flip(img, 1)
        hands = detector.findHands(img,draw = False)

        id1, coor1, hand1 = SingleTracking.Track( hands, img, id1, coor1, hand1, mot_tracker )

        # hand gesture
        if success:
            GameFPS = int(gestureController.GetFPS())
            cv2.putText(img, str(GameFPS), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (151, 166, 134), 3)
                
            if hand1:
                predict_hand = getPredict( hand1, img )
                gestureController.Update(id1, img, predict_hand, *hand1['lmList'])
                if (id1 != -1):
                    cv2.putText(img, "Player", (coor1[0]+20,coor1[1]-10), cv2.FONT_HERSHEY_PLAIN, 3, (151, 0, 0), 3)

            cv2.putText( img, str(int(gestureController.GetStep())), (100, 70), cv2.FONT_HERSHEY_PLAIN, 3, (156, 53, 58), 3 )
            cv2.imshow('img', img)

            pt = Ttime.time()
            DinoGame.SetSpeed(gestureController.GetVelocity()*5, GameFPS)
            DinoGame.SetPlayerState(gestureController.GetHandGesture())

            # UPDATE
            keep = DinoGame.UpDate()
        
        if keep == False:
            run = False

        if cv2.waitKey(1) == ord('q'):
            run = False

def main():
    
    cap = cv2.VideoCapture(0)
    detector = HandDetector(mode=False, # 靜態圖模式，若爲True，每一幀都會調用檢測方法，導致檢測很慢
                        maxHands=4, # 最多檢測幾隻手
                        detectionCon=0.8, # 最小檢測置信度
                        minTrackCon=0.5)  # 最小跟蹤置信度

    gestureController1 = HandDetectController.GestureController()
    gestureController2 = HandDetectController.GestureController() 

    run = True
    P1Control = DinoPlayer1.DinoGameP1()
    P2Control = DinoPlayer2.DinoGameP2()
    BGControl = DinoBG.DinoGameBG()
    clock = time.Clock()

    mot_tracker = sort.Sort() #create instance of the SORT tracker
    id1 = 0
    id2 = 0
    coor1 = []
    coor2 = []
    hand1 = {}
    hand2 = {}

    sc_xPos = 0
    sc_width = 0
    is_change = True
    is_gameover = False

    while run:
        
        # Get Input
        clock.tick(FPS)
        run = P1Control.IsExist()     
        # 返回圖像是否讀取成功，以及讀取的幀圖像img
        success, img = cap.read()

        img = cv2.flip(img, 1) # img垂直翻轉
        # 獲取手部關鍵點信息
        # 檢測手部信息，返回手部關鍵點信息hands字典，繪製關鍵點和連線後的圖像img
        hands = detector.findHands(img,draw = False)

        id1, id2, coor1, coor2, hand1, hand2 = tracking.Track( hands, img, id1, id2, coor1, coor2, hand1, hand2, mot_tracker )

        # hand gesture
        if success:
            GameFPS = int(gestureController1.GetFPS())
            cv2.putText(img, str(GameFPS), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (151, 166, 134), 3)
            gestureController2.GetFPS()

            if hand1:
                predict_hand1 = getPredict( hand1, img )
                gestureController1.Update(img, id1, predict_hand1, *hand1['lmList'])
                if (id1 != -1):
                    cv2.putText(img, "1P", (coor1[0]+20,coor1[1]-10), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3)

            if hand2:
                predict_hand2 = getPredict( hand2, img )
                gestureController2.Update(img, id2, predict_hand2, *hand2['lmList'])
                if (id2 != -1):
                    cv2.putText(img, "2P", (coor2[0]+20,coor2[1]-10), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
                              
            cv2.putText( img, str(int(gestureController1.GetStep())), ( 100, 70 ), cv2.FONT_HERSHEY_PLAIN, 3, ( 156, 53, 58 ), 3 )
            cv2.putText( img, str(int(gestureController2.GetStep())), ( 170, 70 ), cv2.FONT_HERSHEY_PLAIN, 3, ( 156, 53, 58 ), 3 )
            cv2.imshow('img', img)

            if gestureController1.GetVelocity() > gestureController2.GetVelocity():
                GameSpeed2 = BGControl.SetSpeed(gestureController2.GetVelocity()*10, GameFPS)
                GameSpeed1 = BGControl.SetSpeed(gestureController1.GetVelocity()*10, GameFPS) 
                diff = (GameSpeed1 - GameSpeed2) / 10
                
                P1Control.SetSpeed(gestureController1.GetVelocity()*10, 0)
                P2Control.SetSpeed( gestureController2.GetVelocity()*10, diff)

            else:
                GameSpeed1 = BGControl.SetSpeed(gestureController1.GetVelocity()*10, GameFPS)
                GameSpeed2 = BGControl.SetSpeed(gestureController2.GetVelocity()*10, GameFPS)
                diff = (GameSpeed2 - GameSpeed1) / 10

                P2Control.SetSpeed(gestureController2.GetVelocity()*10, 0)
                P1Control.SetSpeed( gestureController1.GetVelocity()*10, diff)  
            
            P1Control.SetPlayerState(gestureController1.GetHandGesture())
            P2Control.SetPlayerState(gestureController2.GetHandGesture())     

            P1XPos, P1isAlive = P1Control.UpDate(sc_xPos, sc_width, is_change)
            P2XPos, P2isAlive = P2Control.UpDate(sc_xPos, sc_width, is_change)

            if P1isAlive == False or P2isAlive == False:
                is_gameover = True

            sc_xPos, sc_width, is_change = BGControl.UpDate(P1XPos, P2XPos, P1isAlive, P2isAlive)
            


        if cv2.waitKey(1) == ord('q'):
            run = False
            gestureController1.CloseFile()


if __name__ == '__main__':
    keep = True

    while keep:
        mode = Mode.modePage() 
        start.startPage()
        if mode == 0:
            single()
        elif mode == 1:
            main() 
