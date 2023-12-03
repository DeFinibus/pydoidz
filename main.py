import pygame
import gameconst
import starfield
import gameobject
import random
import os

def update_score(font,score):
    scr_image = font.render("SCORE:{}".format(score),True,(0,255,0))
    return scr_image
def render_score(screen,scr_image):
    screen.blit(scr_image,(10,1))

# pygame setup
pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((gameconst.SCREEN_W, gameconst.SCREEN_H))
pygame.display.set_caption("PyDoidz 0.1")
pygame.mouse.set_visible(False)
clock = pygame.time.Clock()
running = True
dt = 0
size = 20.0
dir = 0.2
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() - size - 10)

starfield = starfield.Starfield(gameconst.NUM_STARS)
obuhandleri = gameobject.obuhandler()
level = 0

## set  up fonts
font1 = pygame.font.SysFont('arial.ttf', 72)
font2 = pygame.font.SysFont('verdana.ttf',48)
font3 = pygame.font.SysFont('consolas.ttf',32)
font4 = pygame.font.SysFont('consolas.ttf',16)

gameState = gameconst.TITLE_SCREEN

# setup texts
img1 = font1.render('PYDOIDZ', True, (0,255,0))
img2 = font2.render('Press space to start',True,(255,255,255))

win_image = font1.render("YOU WON THE GAME, CONGRATS!",True,(255,255,255))
lose_image = font1.render("GAME OVER!",True,(255,255,255))

lvl_cpl_img = font2.render("LEVEL COMPLETED",True,(200,200,200))
next_lvl_img = font2.render("PREPARE FOR NEXT LEVEL..",True,(200,200,200))

cred1 = font4.render("by DeFinibus",True,(0,255,0))
cred2 = font4.render("Title music: \"Electric Rain\" by Eric Matyas",True,(0,255,0))


level_delay = 0
end_counter = 0
player = None
scr_image = None
music_enabled = True
try:
  music = pygame.mixer.Sound(os.path.join("sounds",gameconst.TITLE_MUSIC))
except:
    music_enabled = False
music_playing = False
while running:
    screen.fill(0x0)
    keys = pygame.key.get_pressed()
    ypos = 0
    xpos = 0
    prev_score=0
    if gameState == gameconst.TITLE_SCREEN:
        if music_enabled:
            if music_playing == False:
                music.play()
                music_playing = True
        level = 1
        obuhandleri.level = level
        screen.blit(img1,(gameconst.SCREEN_W/2-img1.get_width()/2,300))
        screen.blit(img2,(gameconst.SCREEN_W/2-img2.get_width()/2,350))
        screen.blit(cred1,(0,gameconst.SCREEN_H-40))
        screen.blit(cred2,(0,gameconst.SCREEN_H-20))

        if keys[pygame.K_SPACE]:
            gameState = gameconst.INITIALIZING
        score = 0
    if gameState == gameconst.INITIALIZING:
        if music_enabled:
            if music_playing == True:
                music.stop()
                music_playing = False
        obuhandleri.initLevel()
        level_delay = 0
        mystery_alien_counter = 0
        ####### Create enemies ######################################################
        num_foes_in_level = int( gameconst.NUM_ENEMIES_PER_LEVEL*(level+1)/2)
        enemy_speed = gameconst.ENEMY_SPEED + level / 2
        for i in range(num_foes_in_level):
            num = random.randrange(0,3)
            foe = gameconst.foes[num]
            if (i % 15) == 0:
                ypos += foe["block_size"]*foe["h"] + gameconst.SPAN
                xpos = 0
            alien  = gameobject.foe(foe,50+xpos,50+ypos,enemy_speed,0,-1)
            xpos += foe["block_size"]*foe["w"] + gameconst.SPAN
            obuhandleri.addGroup(alien)
        fire_counter = 0
        player = gameobject.player(gameconst.player,player_pos.x,player_pos.y,0,0,-1)
        player.score = score
        scr_image = update_score(font3,player.score)
        obuhandleri.addGroup(player)
        obuhandleri.initLevel()
        obuhandleri.set_player(player)
        level_running = True
        gameState = gameconst.RUNNING
    start = clock.get_time()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    starfield.update()
    starfield.render(screen)

    if gameState == gameconst.RUNNING:
        prev_score = player.score
        if(obuhandleri.dead_foes == num_foes_in_level):
            level +=1
            player.update_score(gameconst.LEVEL_SCORE*(level-1))
            obuhandleri.initLevel()
            if level > gameconst.NUM_LEVELS:
                gameState=gameconst.GAME_CLEAR
                end_counter = 0
            else:
                gameState = gameconst.LEVEL_CLEAR
            player.state=gameconst.VANISH
            
        fire_counter=player.move(keys,fire_counter,dt)
        fire_counter += 1

        mystery_alien_counter +=1
        if mystery_alien_counter > gameconst.MYSTERY_ALIEN_DELAY:
            mystery_alien_counter = 0
            if random.random()*100 <=50:
                ufo = gameobject.saucer(gameconst.saucer,0,50,6,0,200)
                obuhandleri.addGroup(ufo)
        score = player.score
        if player.state == gameconst.DEAD:
            obuhandleri.vanish_all_objects()
            gameState = gameconst.GAME_OVER
    if gameState == gameconst.LEVEL_CLEAR:
        level_delay+=1
        screen.blit(lvl_cpl_img,(gameconst.SCREEN_W/2-lvl_cpl_img.get_width()/2,330))
        screen.blit(next_lvl_img,(gameconst.SCREEN_W/2-next_lvl_img.get_width()/2,380))
        if level_delay > gameconst.LEVEL_DELAY:
            gameState = gameconst.INITIALIZING


    if gameState == gameconst.GAME_CLEAR:
        screen.blit(win_image,(100,300))
        end_counter += 1
        if end_counter > gameconst.GAME_CLEAR_WAIT_TIME:
            level = 1
            gameState = gameconst.TITLE_SCREEN
    if gameState == gameconst.GAME_OVER:
        screen.blit(lose_image,(gameconst.SCREEN_W/2-lose_image.get_width()/2,300))
        end_counter += 1
        if end_counter > gameconst.GAME_CLEAR_WAIT_TIME:
            level = 1
            end_counter = 0
            gameState = gameconst.TITLE_SCREEN

    obuhandleri.update(screen)
    if gameState != gameconst.TITLE_SCREEN:
        if prev_score != player.score:
            scr_image = update_score(font3,player.score)
        render_score(screen,scr_image)
    pygame.display.flip()

    dt = clock.tick(60) / 1000
    end = clock.get_time()
pygame.quit()



