import os

PATH = "Assets/"

IMAGES = {
    'RUNNING':[os.path.join(PATH, "Dino/DinoRun1.png"), 
               os.path.join(PATH, "Dino/DinoRun2.png") ], 

    'JUMPING':os.path.join(PATH, "Dino/DinoJump.png"),

    'DEAD':os.path.join(PATH, "Dino/DinoDead.png" ),
    
    'RUNNING_P1':[os.path.join(PATH, "Dino/DinoRun1_1P.png"), 
                  os.path.join(PATH, "Dino/DinoRun2_1P.png") ], 

    'RUNNING_P2':[os.path.join(PATH, "Dino/DinoRun1_2P.png"), 
                  os.path.join(PATH, "Dino/DinoRun2_2P.png") ], 

    'JUMPING_P1':os.path.join(PATH, "Dino/DinoJump_1P.png"),

    'JUMPING_P2':os.path.join(PATH, "Dino/DinoJump_2P.png"),

    'DUNKING':[os.path.join(PATH, "Dino/DinoDuck1.png"), 
               os.path.join(PATH, "Dino/DinoDuck2.png")], 

    'SMALL_CACTUS':[os.path.join(PATH, "Cactus/SmallCactus1.png"), 
                    os.path.join(PATH, "Cactus/SmallCactus2.png"),
                    os.path.join(PATH, "Cactus/SmallCactus3.png")],

    'LARGE_CACTUS':[os.path.join(PATH, "Cactus/LargeCactus1.png"),
                    os.path.join(PATH, "Cactus/LargeCactus2.png"),
                    os.path.join(PATH, "Cactus/LargeCactus3.png")],

    'BIRD':[os.path.join(PATH, "Bird/Bird1.png"), 
            os.path.join(PATH, "Bird/Bird2.png")],

    'CLOUD':os.path.join(PATH, "Other/Cloud.png"),

    'HEART':os.path.join(PATH, "Other/Heart.png"),

    'BG':os.path.join(PATH, "Other/Track.png"),

    'GAMEOVERBG':os.path.join(PATH, "Other/gameover_background.png"),

    'GAMEOVER':os.path.join(PATH, "Other/GameOver2.png"),

    'P1WIN':os.path.join(PATH, "Other/player1win.png"),

    'P2WIN':os.path.join(PATH, "Other/player2win.png"),

    'Reset':os.path.join(PATH, "Other/Reset.png")
}


# Game Setting

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100 

GROUND_HEIGHT1 = 330

WHITE = (255, 255, 255)
COLOR = WHITE
FPS = 30