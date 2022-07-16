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

colours = np.random.rand(32,3) #32x3的随机矩阵，用于显示用
colours = colours*100000%255

def Similarity( hands, oldhand ):
    if ( oldhand ):
        t = len( hands ) - 1
        while ( t >= 0 ):
            o = np.array( hands[t]['lmList'] )
            o2 = np.array( oldhand['lmList'] )
            co = cosine_similarity( o.reshape(1,-1), o2.reshape(1,-1) )
            print( co )
            if ( (co[0][0] >= 0.9) and (hands[t]['type'] == oldhand['type']) ):
                return t
            t = t - 1

    return -1

def Track( hands, img, id1, id2, coor1, coor2, hand1, hand2, mot_tracker ):
    if len(hands) > 1:
        x, y, w, h = hands[0]['bbox']
        dets = [[x, y, w, h]]
        for i in range(1,len(hands)):
            x, y, w, h = hands[i]['bbox']
            aBbox = [[x, y, w, h]]
            dets = np.append(dets, aBbox,axis= 0)

        dets[:,2:4] += dets[:,0:2] #convert to [x1,y1,w,h] to [x1,y1,x2,y2]
        print(dets)

        start_time = time.time()
        trackers, handList = mot_tracker.update(hands, dets)#利用检测的结果更新跟踪器,返回一个5个数的数组
        cycle_time = time.time() - start_time
        #total_time += cycle_time
        print(len(trackers))

        findco1 = False
        findco2 = False
        miss = []
        missHand = []
        index = 0

        for d in trackers:
            print('%d,%.2f,%.2f,%.2f,%.2f,1,-1,-1,-1'%(d[4],d[0],d[1],d[2]-d[0],d[3]-d[1]))
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

        print( "=====================" )
        print( id1 )
        print( id2 )

        return id1, id2, coor1, coor2, hand1, hand2

    elif len(hands) == 1:
        x, y, w, h = hands[0]['bbox']
        dets = [[x, y, x+w, y+h]]
        print(dets)
        #dets[2:4] += dets[0:2] #convert to [x1,y1,w,h] to [x1,y1,x2,y2]
        trackers, handList = mot_tracker.oneHand(hands, dets)
        print(len(trackers))

        findco1 = False
        findco2 = False
        miss = []
        missHand = []
        index = 0
        for d in trackers:
            print('%d,%.2f,%.2f,%.2f,%.2f,1,-1,-1,-1'%(d[4],d[0],d[1],d[2]-d[0],d[3]-d[1]))
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

        print( "=====================" )
        print( id1 )
        print( id2 )

        return id1, id2, coor1, coor2, hand1, hand2

    else:
        return id1, id2, coor1, coor2, hand1, hand2