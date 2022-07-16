import cv2
import HandTrackingModule as HandTracker
import HandDetectController
import DinoPlayer1
import DinoPlayer2
import DinoBG
from pygame import time
import time as Ttime
from cvzone.HandTrackingModule import HandDetector
import Sort
import numpy as np
from skimage import io
from sklearn.metrics.pairwise import cosine_similarity
import Tracking

FPS = 30

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

    while run:
        
        # Get Input
        clock.tick(FPS)
        run = P1Control.IsExist()     
        # 返回圖像是否讀取成功，以及讀取的幀圖像img
        success, img = cap.read()

        #img = cv2.flip(img, 1) # img垂直翻轉
        # 獲取手部關鍵點信息
        # 檢測手部信息，返回手部關鍵點信息hands字典，繪製關鍵點和連線後的圖像img
        hands, img = detector.findHands(img)
        id1, id2, coor1, coor2, hand1, hand2 = tracking.Track( hands, img, id1, id2, coor1, coor2, hand1, hand2, mot_tracker )
        #handLandMarkPosition = detector.GetPosition(img, draw = False)
        # hand gesture
        if success:
            GameFPS = int(gestureController1.GetFPS())
            cv2.putText(img, str(GameFPS), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (151, 166, 134), 3)
            gestureController2.GetFPS()
            if hand1:   
                gestureController1.Update(img, *hand1['lmList'])
                   
            if hand2:
                # print("p2")
                gestureController2.Update(img, *hand2['lmList'])
                              
            cv2.putText( img, str(int(gestureController1.GetStep())), ( 100, 70 ), cv2.FONT_HERSHEY_PLAIN, 3, ( 156, 53, 58 ), 3 )
            cv2.putText( img, str(int(gestureController2.GetStep())), ( 170, 70 ), cv2.FONT_HERSHEY_PLAIN, 3, ( 156, 53, 58 ), 3 )
            cv2.imshow('img', img)

            if gestureController1.GetVelocity() > gestureController2.GetVelocity():
                BGControl.SetSpeed(gestureController1.GetVelocity()*10, GameFPS)
            else:
                BGControl.SetSpeed(gestureController2.GetVelocity()*10, GameFPS)

            P1Control.SetSpeed(gestureController1.GetVelocity()*10)
            P1Control.SetPlayerState(gestureController1.GetHandGesture())
            
            P2Control.SetSpeed(gestureController2.GetVelocity()*10)
            P2Control.SetPlayerState(gestureController2.GetHandGesture())

            P1XPos = P1Control.UpDate()
            P2XPos = P2Control.UpDate()
            print("P1XPos:", P1XPos, "/ P2XPos:", P2XPos)

            BGControl.UpDate(P1XPos, P2XPos)
            


        if cv2.waitKey(1) == ord('q'):
            run = False


if __name__ == '__main__':
    main() 
