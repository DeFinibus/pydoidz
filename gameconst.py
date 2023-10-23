SCREEN_W = 1024
SCREEN_H = 768

NUM_STARS = 100

#do not mess with these ###
ALIVE = 0
DEAD = 1
DYING = 2
VANISH = 3

TITLE_SCREEN = 0
INITIALIZING = 1
RUNNING = 2
LEVEL_CLEAR = 3
GAME_CLEAR = 4
GAME_OVER = 5

#############################

FIRE_DELAY = 30

NUM_ENEMIES_PER_LEVEL = 15
NUM_LEVELS = 6
SPAN = 16
FOE_FIRE_DELAY = 180

ENEMY_SPEED = 2
ENEMY_FIRE_RATE = 30
## FOE MODES
FOE_NORMAL = 0
FOE_ATTACK = 1

###
MISSILE_LIFE = 100

LEVEL_DELAY = 200
GAME_CLEAR_WAIT_TIME = 400
MYSTERY_ALIEN_DELAY = 500
########### POINTS #####################
FOE_BASE_SCORE = 50
LEVEL_SCORE = 1000


palette=[0x000000, #0 black 
         0xFFFFFF, #1 white
         0xFF0000, #2 red
         0x00FF00, #3 green
         0x0000FF, #4 blue
         0xFF7F00, #5 orange
         0x7F4000, #6 brown
         0x7F7F7F, #7 grey
         0xACACAC,  #8 light grey
         0x373737  #9 dark grey
         ] 
foes =[ {"w":8,
         "h":8,
         "block_size":4,
         "color":0xFF3300,
         "data":[
             3,0,0,0,0,0,0,3,
             3,3,0,0,0,0,3,3,
             3,3,3,3,3,3,3,3,
             3,3,3,3,3,3,3,3,
             3,3,0,3,3,0,3,3,
             3,3,3,5,5,3,3,3,
             8,3,0,3,3,0,3,8,
             8,0,0,0,0,0,0,8
         ]
         },
         {"w":8,
         "h":8,
         "block_size":4,
         "color":0x22FF22,
         "data":[
             0,0,0,4,4,0,0,0,
             4,4,0,4,4,0,4,4,
             4,4,2,2,2,2,4,4,
             0,0,4,4,4,4,0,0,
             0,4,0,4,4,0,4,0,
             4,4,4,4,4,4,4,4,
             4,4,0,4,4,0,4,4,
             4,0,0,4,4,0,0,4
         ]
         },
         {"w":8,
         "h":8,
         "block_size":4,
         "color":0x22FF22,
         "data":[
             0,0,0,6,6,0,0,0,
             0,0,5,6,6,5,0,0,
             0,5,5,5,5,5,5,0,
             5,5,6,6,6,6,5,5,
             5,5,5,5,5,5,5,5,
             0,5,5,5,5,5,5,0,
             0,0,6,6,6,6,0,0,
             0,0,0,6,6,0,0,0
         ]
         }

]
player = {"w":8,
         "h":8,
         "block_size":4,
         "color":0xAAAAAA,
         "data":[
             0,0,0,0,0,0,0,0,
             0,0,0,1,1,0,0,0,
             0,0,7,8,8,7,0,0,
             0,7,7,0,0,7,7,0,
             0,8,7,7,7,7,8,0,
             8,7,7,7,7,7,7,8,
             0,0,0,8,8,0,0,0,
             0,8,7,7,7,7,8,0
         ]
         }
saucer = {"w":16,
         "h":8,
         "block_size":4,
         "color":0xAAAAAA,
         "data":[
             0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
             0,0,0,7,7,7,7,7,7,7,7,7,7,0,0,0,
             0,0,7,8,8,8,8,8,8,8,8,8,8,7,0,0,
             7,8,8,8,1,1,1,1,1,1,1,8,8,8,8,7,
             7,8,8,8,8,8,8,8,8,8,8,8,8,8,8,7,
             0,0,7,7,8,8,8,8,8,8,8,8,7,7,0,0,
             0,0,0,8,8,7,7,7,7,7,7,7,7,7,0,0,
             0,0,0,0,0,9,9,9,9,9,9,9,0,0,0,0
         ]
         }
sounds = {
    "GUN":{"file":"ProjectileShoot.wav","id":0},
    "EXPLOSION":{"file":"EXP2.WAV","id":1},
    "FOE_GUN":{"file":"fire_03.wav","id":3}
}
TITLE_MUSIC = "Electric_Rain.mp3"
