import pygame
import random
import cfg

pygame.init()
SCREEN = pygame.display.set_mode((cfg.SCREEN_WIDTH, cfg.SCREEN_HEIGHT)) # 設定視窗

class Cloud():
    def __init__(self):
        self.xPos = cfg.SCREEN_HEIGHT + random.randint(800, 1000)
        self.yPos = random.randint(50, 100)
        self.display_img = pygame.image.load(cfg.IMAGES['CLOUD'])
        self.width = self.display_img.get_width()

    def Update(self, speed, XPos):
        if XPos < 780:
            self.xPos -= speed / 4
        else:
            self.xPos -= speed / 2 

        if ( self.xPos < -self.width ):
            self.xPos = cfg.SCREEN_WIDTH + random.randint(800, 2000)
            self.yPos = random.randint(50, 100)

    def Draw(self):
        SCREEN.blit(self.display_img, (self.xPos, self.yPos))

class BackGround():
    def __init__(self):
        self.xPos = 0
        self.yPos = 380
        self.display_img = pygame.image.load(cfg.IMAGES['BG'])
        self.width = self.display_img.get_width() 

    def Update(self, speed, XPos):
        if XPos < 780:
            self.xPos -= speed / 2
        else:
            self.xPos -= speed / 1.5 

        if ( self.xPos <= -self.width ):
            self.xPos = 0

    def Draw(self):
        SCREEN.blit(self.display_img, (self.xPos, self.yPos))
        SCREEN.blit(self.display_img, (self.width + self.xPos, self.yPos))

class Bird():
    def __init__(self):
        self.xPos = cfg.SCREEN_WIDTH
        self.yPos = 250
        self.fly_img = []

        for value in cfg.IMAGES['BIRD']:
            self.fly_img.append(pygame.image.load(value))

        self.display_img = self.fly_img[0]
        self.fly_index = 0
        self.flyingSpeed = 5

    def Update( self, speed, XPos):
        if XPos < 780: # 未到達錨點
            self.xPos -= ( self.flyingSpeed + speed / 4 )
        else:
            self.xPos -= ( self.flyingSpeed + speed / 2 )

        if ( self.xPos <= -self.display_img.get_width() ):
            self.xPos = cfg.SCREEN_WIDTH + random.randint(100, 2000)
            self.yPos = random.randint( 250, 270 )
        
        self.Fly()
        if ( self.fly_index >= 10 ):
            self.fly_index = 0

    def Fly( self ):
        self.display_img = self.fly_img[ self.fly_index // 5 ]
        self.fly_index += 1

    def Draw(self):
        SCREEN.blit( self.display_img, (self.xPos, self.yPos) )

class LargeCactus():
    def __init__(self):
        
        self.xPos = cfg.SCREEN_WIDTH
        self.yPos = cfg.GROUND_HEIGHT1

        self.cactus_img = []
        for value in cfg.IMAGES['LARGE_CACTUS']:
            self.cactus_img.append(pygame.image.load(value))

        self.cactusNumber = random.randint(0, 2)
        self.display_img = self.cactus_img[self.cactusNumber]
        
    def Update(self, speed, XPos):
        if XPos < 780:
            self.xPos -= speed / 4
        else:
            self.xPos -= speed / 2

        if ( self.xPos <= -self.display_img.get_width() ):
            self.xPos = cfg.SCREEN_WIDTH + random.randint(100, 1000)
            self.cactusNumber = random.randint(0, 2)
            self.display_img = self.cactus_img[self.cactusNumber]

    def Draw(self):
        SCREEN.blit(self.display_img, (self.xPos, self.yPos))

class SmallCactus():
    def __init__(self):
        
        self.xPos = random.randint(100, cfg.SCREEN_WIDTH)
        self.yPos = cfg.GROUND_HEIGHT1

        self.cactus_img = []
        for value in cfg.IMAGES['SMALL_CACTUS']:
            self.cactus_img.append(pygame.image.load(value))

        self.cactusNumber = random.randint(0, 2)
        self.display_img = self.cactus_img[self.cactusNumber]
        
    def Update(self, speed, XPos):
        if XPos < 780:
            self.xPos -= speed / 4.5
        else:
            self.xPos -= speed / 2.5

        if ( self.xPos <= -self.display_img.get_width() ):
            self.xPos = cfg.SCREEN_WIDTH + random.randint(100, 1000)
            self.cactusNumber = random.randint(0, 2)
            self.display_img = self.cactus_img[self.cactusNumber]

    def Draw(self):
        SCREEN.blit(self.display_img, (self.xPos, self.yPos))

class DinoGameBG():

    def __init__(self): 
        self.GAMESPEED = 0
        self.clock = pygame.time.Clock()
        self.pre_fps = 20

        self.cloud = Cloud()
        self.bg = BackGround()
        self.bird = Bird()
        self.smallCactus1 = SmallCactus()
        self.largeCactus1 = LargeCactus()

    def UpDate(self, P1XPos, P2XPos):
        if P1XPos >= P2XPos:
            XPos = P1XPos
        else:
            XPos = P2XPos

        self.cloud.Draw()
        self.cloud.Update(self.GAMESPEED, XPos)
        self.bg.Draw()
        self.bg.Update(self.GAMESPEED, XPos)
        self.bird.Draw()
        self.bird.Update( self.GAMESPEED, XPos)
        self.smallCactus1.Draw()
        self.smallCactus1.Update(self.GAMESPEED, XPos)
        self.largeCactus1.Draw()
        self.largeCactus1.Update(self.GAMESPEED, XPos)

        pygame.display.update()

    def SetSpeed(self, speed, fps):
        if fps >=20:
            self.GAMESPEED = speed 
        else:
            self.GAMESPEED = speed*(20 - fps)*0.7 + self.pre_fps*0.3

        self.pre_fps = fps

    def IsExist(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True