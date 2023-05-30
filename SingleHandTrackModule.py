import cv2
import mediapipe as mp

class HandDetector():

    def __init__( self, mode = False, maxHands = 2, complexity = 1, detectionConfidence = 0.5, trackingConfidence = 0.5 ):
        self.mode = mode
        self.maxHands = maxHands
        self.complexity = complexity
        self.detectionConfidence = detectionConfidence
        self.trackingConfidence = trackingConfidence
        
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands( static_image_mode = self.mode,
                                         max_num_hands = self.maxHands, 
                                         model_complexity = self.complexity ,
                                         min_detection_confidence = self.detectionConfidence,
                                         min_tracking_confidence = self.trackingConfidence )
        self.mpDraw = mp.solutions.drawing_utils


    def FindHands( self, img, draw = True ): # Find out all of hands in the image

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # BGR to RGB
        self.result = self.hands.process(imgRGB) 

        if self.result.multi_hand_landmarks: #detect wheather the hand detect
            for handLms in self.result.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS) #draw in img   

        return img

    def GetPosition( self, img, handNo = 0, draw = False ):
        handLandMarkPosition = []

        imgWidth = img.shape[0]
        imgHeight = img.shape[1]
        if self.result.multi_hand_landmarks:
            theHand = self.result.multi_hand_landmarks[handNo]

            for id, lm in enumerate(theHand.landmark):
                
                xPos = int(lm.x * imgWidth)
                yPos = int(lm.y * imgHeight)
                
                handLandMarkPosition.append([id, xPos, yPos])

                if draw:
                    if ( id == self.mpHands.HandLandmark.INDEX_FINGER_TIP and id == self.mpHands.HandLandmark.MIDDLE_FINGER_TIP ):
                        cv2.circle( img, (xPos, yPos), 15, (255, 255, 255), cv2.FILLED )

        return handLandMarkPosition


                    
                    
        

