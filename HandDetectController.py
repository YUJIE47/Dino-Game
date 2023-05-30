import enum
import re
import time
import math
import numpy as np
import kf_function

XPOS, YPOS = 0, 1
POS, NEG = 0, 1

class HandLandmark(enum.IntEnum):
  """The 21 hand landmarks."""
  WRIST = 0
  THUMB_CMC = 1
  THUMB_MCP = 2
  THUMB_IP = 3
  THUMB_TIP = 4
  INDEX_FINGER_MCP = 5
  INDEX_FINGER_PIP = 6
  INDEX_FINGER_DIP = 7
  INDEX_FINGER_TIP = 8
  MIDDLE_FINGER_MCP = 9
  MIDDLE_FINGER_PIP = 10
  MIDDLE_FINGER_DIP = 11
  MIDDLE_FINGER_TIP = 12
  RING_FINGER_MCP = 13
  RING_FINGER_PIP = 14
  RING_FINGER_DIP = 15
  RING_FINGER_TIP = 16
  PINKY_MCP = 17
  PINKY_PIP = 18
  PINKY_DIP = 19
  PINKY_TIP = 20

class GestureController():

    def __init__( self ) :
        self.distanceState = POS # record positvie or negative
        self.step = 0
        self.preTimeRecordStep = 0
        self.velocity = 0
        self.curTime = 0
        self.preTime = 0
        self.perSecondStaringTime = time.time()
        self.id = 0
        self.vlist = []
        self.stone = 0
        self.not_stone = 0
        self.P0 = np.array([[1, 0], [0, 1]])
        self.X0 = np.array([self.velocity, 1.0])
        self.alist = []
        self.orv = 0

        self.curHandGesture = "STOP"

    # Update function is to recognize gesture detection
    # and update result per frame
    def Update(self, img, id, predict, *handLandMarkPosition):
        self.handLandMarkPosition = handLandMarkPosition

        if len(self.handLandMarkPosition) != 0 :
            if (self.IsReady()):
                
                self.IsOneStep(distanceTurnOut = 1)

                self.curHandGesture = "RUNNING" # return hand gesture

                if self.IsJump2( predict ):
                    self.curHandGesture = "JUMPING" # return hand gesture
                
                if (self.IsOneSecond()):
                    self.CalculatingVelocity(0.7, 0.3, id)
                    self.id = id   

        elif ( self.IsOneSecond() ):
            self.CalculatingVelocity( 0.15, 0.85, id)
            self.id = id

    # Get current hand gesture
    def GetHandGesture(self):
        return self.curHandGesture 

    # To calculate the speed of the finger race
    def CalculatingVelocity( self, a , b , id ):
        Bias = ( self.step - self.preTimeRecordStep )
        
        if self.id < 0 and id < 0: # 持續1秒鏡頭為偵測到手
            self.velocity = round((self.velocity*a + Bias*b), 1)
            self.orv = round((self.orv*a + Bias*b), 1)
        elif Bias != 0:
            self.velocity = round((self.velocity*a + Bias*b), 1) # normalize the velocity
            self.orv = round((self.orv*a + Bias*b), 1)

        self.X0 = kf_function.kf( self.X0, self.P0, self.orv )
        self.velocity = self.X0[0]
        self.preTimeRecordStep = self.step


    # To detect if is passing one second
    def IsOneSecond( self ) :
        if ( (self.curTime - self.perSecondStaringTime) >= 1 ):
            self.perSecondStaringTime = self.curTime
            return True
        else:
            return False
    
    # To Initialize the recording seconde which is used to calculate if is one second
    def InitPerSecondStartingTime(self):
        self.perSecondStaringTime = self.curTime

    # To get the game fps
    def GetFPS( self ):
        self.curTime = time.time()
        fps = 1 / (self.curTime - self.preTime )
        self.preTime = self.curTime

        return fps

    # To get the current recording step
    def GetStep( self ):
        return self.step

    # To get the velocity of per step 
    def GetVelocity( self ):
        return self.velocity

    # Recognizing gesture function
    # To detect if is the palm down
    def IsReady( self ) :
        if ( self.handLandMarkPosition[HandLandmark.INDEX_FINGER_TIP][YPOS] > self.handLandMarkPosition[HandLandmark.WRIST][YPOS] and
             self.handLandMarkPosition[HandLandmark.MIDDLE_FINGER_TIP][YPOS] > self.handLandMarkPosition[HandLandmark.WRIST][YPOS] ):
            return True

        else:
            return False
    
    def IsJump2( self, predict ):
        if ( predict == 0 ):
            self.not_stone = self.not_stone + 1
            if ( self.stone > 0 ):
                if ( self.not_stone >= 3 ):
                    self.stone = 0
                    self.not_stone = 0

        elif ( predict == 1 ):
            self.stone = self.stone + 1
            if ( self.stone >= 2 ):
                print("jump!!!")
                self.stone = 0
                self.not_stone = 0
                return True
        return False

    def IsJump(self, jumpTurnOut=2 ):
        self.IndexFinger_TIP2PIP = self.Get_YPOS_Distance(HandLandmark.INDEX_FINGER_TIP, HandLandmark.INDEX_FINGER_PIP)
        self.IndexFinger_PIP2MCP = self.Get_YPOS_Distance(HandLandmark.INDEX_FINGER_PIP, HandLandmark.INDEX_FINGER_MCP)
        self.MiddleFinger_TIP2PIP = self.Get_YPOS_Distance(HandLandmark.MIDDLE_FINGER_TIP, HandLandmark.INDEX_FINGER_PIP)
        self.MiddleFinger_PIP2MCP = self.Get_YPOS_Distance(HandLandmark.MIDDLE_FINGER_PIP, HandLandmark.MIDDLE_FINGER_MCP)

        if ( self.IndexFinger_TIP2PIP < self.IndexFinger_PIP2MCP/jumpTurnOut and self.MiddleFinger_TIP2PIP < self.MiddleFinger_PIP2MCP/jumpTurnOut ):
            return True
    
        return False

    # Get a value(residual) to make sure the hand isn't effected by moving front and back(z position) 
    def NormalizingViewer(self, distance ):
        self.residual = self.CalculateDisplacement( HandLandmark.INDEX_FINGER_MCP, HandLandmark.WRIST )
        if self.residual != 0 :
            distance /= self.residual
            result = round( distance, 3 )
            return result

        return 0 

    # To identity if is one step
    # 
    # distanceTunrOut is to set the two finger which see as legs in finger race
    # need to distance between the value( distanceTurnOut ) 
    def IsOneStep( self, distanceTurnOut = 1 ):
        
        distance = self.Get_XPOS_Distance( HandLandmark.INDEX_FINGER_TIP, HandLandmark.MIDDLE_FINGER_TIP )
        normalizeDistance = self.NormalizingViewer( distance )

        if ( normalizeDistance >= 0 and self.distanceState == NEG ):
            if ( abs( normalizeDistance ) > distanceTurnOut ):
                self.step += 1
                self.distanceState = POS

        elif ( normalizeDistance < 0 and self.distanceState == POS ):
            if ( abs( normalizeDistance ) > distanceTurnOut ):
                self.step += 1
                self.distanceState = NEG

    # To calculate the distance between X1 and X2
    def Get_XPOS_Distance( self, landMark1, landMark2 ):
        return ( self.handLandMarkPosition[landMark1][XPOS] - self.handLandMarkPosition[landMark2][XPOS] )
    
    def Get_YPOS_Distance( self, landMark1, landMark2 ):
        return ( self.handLandMarkPosition[landMark1][YPOS] - self.handLandMarkPosition[landMark2][YPOS] )
    
    # Get the displancement between two point (X1, Y1) ( X2, Y2 )
    def CalculateDisplacement( self, landMark1, landMark2 ):
        result = math.sqrt(abs(( self.Get_XPOS_Distance(landMark1, landMark2) )^2 - self.Get_YPOS_Distance(landMark1, landMark2)^2))
        return round( result, 3 ) 
