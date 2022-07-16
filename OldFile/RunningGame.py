import cv2
import time
import HandTrackingModule as HandTracker
import GameController as Game
    

def main():
    
    curTime, preTime = 0, 0

    cap = cv2.VideoCapture(0)
    detector = HandTracker.HandDetector(  )
    controller = Game.GameControl()

    while True:

        success, img = cap.read()

        #img = cv2.flip(img, 1)
        img = detector.FindHands(img, True)
        handLandMarkPosition = detector.GetPosition(img)

        if len(handLandMarkPosition) != 0 :
            #print(handLandMarkPosition[4])
            controller.Run(img, *handLandMarkPosition)
            cv2.putText( img, str(int(controller.GetStep())), ( 100, 70 ), cv2.FONT_HERSHEY_PLAIN, 3, ( 156, 53, 58 ), 3 )

        if success:
            
            # Calculate FPS
            curTime = time.time()
            fps = 1 / (curTime - preTime )
            preTime = curTime
            cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (151, 166, 134), 3)

            cv2.imshow('img', img)

        if cv2.waitKey(1) == ord('q'):
            break


if __name__ == '__main__':
    main() 
