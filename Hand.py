from __future__ import print_function

import os
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from skimage import io
from sklearn.metrics.pairwise import cosine_similarity

import glob
import argparse
from filterpy.kalman import KalmanFilter

import cv2
from cvzone.HandTrackingModule import HandDetector
import time
import math

import sort
from sklearn.metrics.pairwise import cosine_similarity

def Similarity( hands, oldhand ):
  if ( oldhand ):
    t = len( hands ) - 1
    while ( t >= 0 ):

      o = np.array( hands[t]['lmList'] )
      o2 = np.array( oldhand['lmList'] )
      co = cosine_similarity( o.reshape(1,-1), o2.reshape(1,-1) )
      # print( co )
      if ( (co[0][0] >= 0.9) and (hands[t]['type'] == oldhand['type']) ):
        return t
      t = t - 1

  return -1

#（1）捕獲攝像頭
cap = cv2.VideoCapture(0) # 捕獲電腦攝像頭
cap.set(3, 1280)  # 設置顯示窗口寬度1280
cap.set(4, 720)   # 顯示窗口高度720
 
pTime = 0  # 處理第一幀圖像的起始時間
 
#（2）接收手部檢測方法
detector = HandDetector(mode=False, # 靜態圖模式，若爲True，每一幀都會調用檢測方法，導致檢測很慢
                        maxHands=4, # 最多檢測幾隻手
                        detectionCon=0.8, # 最小檢測置信度
                        minTrackCon=0.5)  # 最小跟蹤置信度
 

colours = np.random.rand(32,3) #32x3的随机矩阵，用于显示用
colours = colours*100000%255
mot_tracker = sort.Sort() #create instance of the SORT tracker

id1 = 0
id2 = 0
coor1 = []
coor2 = []
hand1 = {}
hand2 = {}

#（3）處理每一幀圖像
while True:
    total_time = 0.0 #总共耗时
    # 返回圖像是否讀取成功，以及讀取的幀圖像img
    success, img = cap.read()

    #（4）獲取手部關鍵點信息
    # 檢測手部信息，返回手部關鍵點信息hands字典，繪製關鍵點和連線後的圖像img
    hands, img = detector.findHands(img)
    
    #print(hands)    

    if len(hands) > 1:
         
        x, y, w, h = hands[0]['bbox']
        dets = [[x, y, w, h]]

        for i in range(1,len(hands)):
            x, y, w, h = hands[i]['bbox']
            aBbox = [[x, y, w, h]]
            dets = np.append(dets, aBbox,axis= 0)

        dets[:,2:4] += dets[:,0:2] #convert to [x1,y1,w,h] to [x1,y1,x2,y2]
        # print(dets)

        start_time = time.time()
        trackers, handList = mot_tracker.update(hands, dets)#利用检测的结果更新跟踪器,返回一个5个数的数组
        cycle_time = time.time() - start_time
        total_time += cycle_time
        # print(len(trackers))

        findco1 = False
        findco2 = False
        miss = []
        missHand = []
        index = 0
        for d in trackers:
          # print('%d,%.2f,%.2f,%.2f,%.2f,1,-1,-1,-1'%(d[4],d[0],d[1],d[2]-d[0],d[3]-d[1]))
          d = d.astype(np.int32)#转换成整形
          cv2.rectangle( img, (d[0],d[1]), (d[2],d[3]), colours[d[4]%len(trackers),:], 2 )
          cv2.putText(img, str(d[4]), (d[0],d[1]), cv2.FONT_HERSHEY_PLAIN, 3, colours[d[4]%len(trackers),:], 3)
          #rect=patches.Rectangle((d[0],d[1]),d[2]-d[0],d[3]-d[1],fill=False,lw=3,ec=colours[d[4]%32,:])
          if int(d[4]) == id1:
            findco1 = True
            coor1 = d
            hand1 = handList[index]

          elif int(d[4]) == id2:
            findco2 = True
            coor2 = d
            hand2 = handList[index]

          else:
            miss.append(d)
            missHand.append( handList[index] )
          index = index + 1

        if findco1 == False:
          if findco2 == False:
            if miss:
              if len( miss ) > 1:
                in1 = Similarity( missHand, hand1 )
                in2 = Similarity( missHand, hand2 )
                if ( in1 == -1 ):
                  if ( in2 == -1 ):
                    coor1 = miss[0]
                    id1 = int(coor1[4])
                    hand1 = missHand[0]
                    coor2 = miss[1]
                    id2 = int(coor2[4])
                    hand2 = missHand[1]
                  else:
                    coor2 = miss[in2]
                    id2 = int(coor2[4])
                    hand2 = missHand[in2]
                    miss.pop(in2)
                    missHand.pop(in2)
                    coor1 = miss[0]
                    id1 = int(coor1[4])
                    hand1 = missHand[0]
                else:
                  if ( in2 == -1 ):
                    coor1 = miss[in1]
                    id1 = int(coor1[4])
                    hand1 = missHand[in1]
                    miss.pop(in1)
                    missHand.pop(in1)
                    coor2 = miss[0]
                    id2 = int(coor2[4])
                    hand2 = missHand[0]
                  else:
                    coor2 = miss[in2]
                    id2 = int(coor2[4])
                    hand2 = missHand[in2]
                    coor1 = miss[in1]
                    id1 = int(coor1[4])
                    hand1 = missHand[in1]
              else:
                id2 = -1
                in1 = Similarity( missHand, hand1 )
                if ( in1 == -1 ):
                  coor1 = miss[0]
                  id1 = int(coor1[4])
                  hand1 = missHand[0]
                else:
                  coor1 = miss[in1]
                  id1 = int(coor1[4])
                  hand1 = missHand[in1]
            else:
              id1 = -1
              id2 = -1
          else:
            if miss:
              in1 = Similarity( missHand, hand1 )
              if ( in1 == -1 ):
                coor1 = miss[0]
                id1 = int(coor1[4])
                hand1 = missHand[0]
              else:
                coor1 = miss[in1]
                id1 = int(coor1[4])
                hand1 = missHand[in1]
            else:
              id1 = -1

        elif findco2 == False:
          if miss:
            in2 = Similarity( missHand, hand2 )
            if ( in2 == -1 ):
              coor2 = miss[0]
              id2 = int(coor2[4])
              hand2 = missHand[0]
            else:
              coor2 = miss[in2]
              id2 = int(coor2[4])
              hand2 = missHand[in2]
          else:
            id2 = -1

        # print( "=====================" )
        # print( id1 )
        # print( hand1 )
        # print( id2 )
        # print( hand2 )

    elif len(hands) == 1:
        x, y, w, h = hands[0]['bbox']
        dets = [[x, y, x+w, y+h]]
        # print(dets)
        #dets[2:4] += dets[0:2] #convert to [x1,y1,w,h] to [x1,y1,x2,y2]
        trackers, handList = mot_tracker.oneHand(hands, dets)
        # print(len(trackers))

        findco1 = False
        findco2 = False
        miss = []
        missHand = []
        index = 0
        for d in trackers:
          # print('%d,%.2f,%.2f,%.2f,%.2f,1,-1,-1,-1'%(d[4],d[0],d[1],d[2]-d[0],d[3]-d[1]))
          d = d.astype(np.int32)#转换成整形
          cv2.rectangle( img, (d[0],d[1]), (d[2],d[3]), colours[d[4]%len(trackers),:], 2 )
          cv2.putText(img, str(d[4]), (d[0],d[1]), cv2.FONT_HERSHEY_PLAIN, 3, colours[d[4]%len(trackers),:], 3)
          if int(d[4]) == id1:
            findco1 = True
            coor1 = d
            hand1 = handList[index]

          elif int(d[4]) == id2:
            findco2 = True
            coor2 = d
            hand2 = handList[index]

          else:
            miss.append(d)
            missHand.append( handList[index] )
          index = index + 1

        if findco1 == False:
          if findco2 == False:
            if miss:
              if len( miss ) > 1:
                in1 = Similarity( missHand, hand1 )
                in2 = Similarity( missHand, hand2 )
                if ( in1 == -1 ):
                  if ( in2 == -1 ):
                    coor1 = miss[0]
                    id1 = int(coor1[4])
                    hand1 = missHand[0]
                    coor2 = miss[1]
                    id2 = int(coor2[4])
                    hand2 = missHand[1]
                  else:
                    coor2 = miss[in2]
                    id2 = int(coor2[4])
                    hand2 = missHand[in2]
                    miss.pop(in2)
                    missHand.pop(in2)
                    coor1 = miss[0]
                    id1 = int(coor1[4])
                    hand1 = missHand[0]
                else:
                  if ( in2 == -1 ):
                    coor1 = miss[in1]
                    id1 = int(coor1[4])
                    hand1 = missHand[in1]
                    miss.pop(in1)
                    missHand.pop(in1)
                    coor2 = miss[0]
                    id2 = int(coor2[4])
                    hand2 = missHand[0]
                  else:
                    coor2 = miss[in2]
                    id2 = int(coor2[4])
                    hand2 = missHand[in2]
                    coor1 = miss[in1]
                    id1 = int(coor1[4])
                    hand1 = missHand[in1]
              else:
                id2 = -1
                in1 = Similarity( missHand, hand1 )
                if ( in1 == -1 ):
                  coor1 = miss[0]
                  id1 = int(coor1[4])
                  hand1 = missHand[0]
                else:
                  coor1 = miss[in1]
                  id1 = int(coor1[4])
                  hand1 = missHand[in1]
            else:
              id1 = -1
              id2 = -1
          else:
            if miss:
              in1 = Similarity( missHand, hand1 )
              if ( in1 == -1 ):
                coor1 = miss[0]
                id1 = int(coor1[4])
                hand1 = missHand[0]
              else:
                coor1 = miss[in1]
                id1 = int(coor1[4])
                hand1 = missHand[in1]
            else:
              id1 = -1

        elif findco2 == False:
          if miss:
            in2 = Similarity( missHand, hand2 )
            if ( in2 == -1 ):
              coor2 = miss[0]
              id2 = int(coor2[4])
              hand2 = missHand[0]
            else:
              coor2 = miss[in2]
              id2 = int(coor2[4])
              hand2 = missHand[in2]
          else:
            id2 = -1

        # print( "=====================" )
        # print( id1 )
        # print( id2 )

    #（5）圖像顯示
    # 計算FPS值
    cTime = time.time()  # 處理一幀圖像所需的時間
    fps = 1/(cTime-pTime) 
    pTime = cTime  # 更新處理下一幀的起始時間
    
    # 把fps值顯示在圖像上,img畫板,顯示字符串,顯示的座標位置,字體,字體大小,顏色,線條粗細
    cv2.putText(img, str(int(fps)), (50,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,0), 3)

    # 顯示圖像，輸入窗口名及圖像數據
    # cv2.namedWindow("img", 0)  # 窗口大小可手動調整
    cv2.imshow('img', img)

    if cv2.waitKey(20) & 0xFF==27:  #每幀滯留20毫秒後消失，ESC鍵退出
        break
 
# 釋放視頻資源
cap.release()
cv2.destroyAllWindows()