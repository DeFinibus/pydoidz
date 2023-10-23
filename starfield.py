
import pygame

import random
import gameconst


class Star(object):
    def __init__(self,x,y,speed):
        self.x = x
        self.y = y
        self.speed = speed

class Starfield(object):
    def __init__(self, num_stars):
        self.stars = []
        for i in range(num_stars):
            x = random.randrange(0,int(gameconst.SCREEN_W))
            y = random.randrange(0,int(gameconst.SCREEN_H))
            speed = random.random()*3.5+0.5
            star = Star(x,y,speed)
            self.stars.append(star)
    def update(self):
        for i in range(len(self.stars)):
            self.stars[i]. y += self.stars[i].speed
            if(self.stars[i].y > gameconst.SCREEN_H):
                self.stars[i].y = 0
                #self.stars[i].y = random.randrange(0,int(gameconst.SCREEN_H))
    def render(self,screen):
        for i in range(len(self.stars)):
            x = self.stars[i].x
            y = self.stars[i].y
            size = self.stars[i].speed+0.5
            c = 60*self.stars[i].speed
            pygame.draw.rect(screen,(c,c,c),(x,y,1,1))
            
