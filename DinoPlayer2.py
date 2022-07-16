import pygame
import cfg

pygame.init()
SCREEN = pygame.display.set_mode((cfg.SCREEN_WIDTH, cfg.SCREEN_HEIGHT)) # 設定視窗

class DinoPlayer2():

    DinoXPos = 50
    DinoYPos = 240
    RunPlacement = 5
    JumpingPlacement = 30
    FallingVelocity = 3

    def __init__(self):
        self.run_img = []
        for value in cfg.IMAGES['RUNNING_P2']:
            self.run_img.append(pygame.image.load(value)) # loading the running image
        self.jump_img = pygame.image.load( cfg.IMAGES['JUMPING_P2'] ) # loading the jumping image

        self.run_state = True
        self.jump_state = False
        self.displacement = 0
        self.pre_speed = 0
        self.difference = 0 

        self.curJumpingVelocity = self.JumpingPlacement
        self.step_index = 0 # record step to switch run1 and run2 image
        self.display_img = self.run_img[0]


    def Update( self, speed ):
        if self.jump_state :
            self.Jump()
        elif self.run_state :
            self.Run( speed )

            if ( self.step_index >= 10 ):   # switch running image 2 to running image 1
                self.step_index = 0
                # print( "P2 diff:", self.displacement)
                self.DinoXPos += ( self.displacement / 1.5 )
                print("P2 displacement:", self.displacement / 1.5)
                self.displacement = 0         # reset to zero 
       
        if ( self.DinoXPos >= 780 ):     # over the anchor
            self.DinoXPos = 780
        elif ( self.DinoXPos <= 80 ):
            self.DinoXPos = 80
        
        return self.DinoXPos


    def Run(self, speed ):
        self.display_img = self.run_img[ self.step_index // 5 ]
        if ( speed > 1 ): # To decide weather the running image need to switch
            self.step_index += 1
            # print( "P2 speed: ", speed, "/ pre_speed: ", self.pre_speed )
            difference = speed - self.pre_speed
            if ( difference == 0 ):
                self.displacement += 1
            elif ( difference > 0 ):
                self.displacement += difference
            elif ( difference < 0 ):
                self.displacement -= difference * 2 
            
            

            self.pre_speed = speed           # update pre_speed
            

    def Jump(self):
        # switch to jumping image
        self.display_img = self.jump_img

        self.DinoYPos -= self.curJumpingVelocity
        self.curJumpingVelocity -= self.FallingVelocity

        # if Dino is Falling to the ground, then stop falling 
        if ( self.curJumpingVelocity < -self.JumpingPlacement ):
            self.curJumpingVelocity = self.JumpingPlacement
            self.jump_state = False

    def Draw(self):
        SCREEN.blit( self.display_img, ( self.DinoXPos, self.DinoYPos ) ) # 繪製覆蓋整個視窗


class DinoGameP2():

    def __init__(self): 
        self.GAMESPEED = 0
        self.clock = pygame.time.Clock()
        self.player = DinoPlayer2()

    def UpDate(self):
        self.player.Draw()
        XPos = self.player.Update( self.GAMESPEED )

        return XPos

    def SetSpeed(self, speed):
        self.GAMESPEED = speed

    def SetPlayerState(self, handGesture):
        #print( handGesture )
        if ( handGesture == "JUMPING" ):
            self.player.jump_state = True

    def IsExist(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True