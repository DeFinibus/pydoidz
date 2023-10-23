import pygame
import gameconst
import uuid
import math
import random          
import os
class obuhandler:
    def __init__(self):
        self.objects = []
        self.groups = []
        self.dead_foes = 0
        self.player = None
        self.level = 1
        self.sounds = {}
        self.load_sounds()
    def initLevel(self):
        self.dead_foes = 0
    def set_player(self,player):
        self.player = player
    def get_player(self):
        return self.player
    def get_player_pos(self):
        return self.player.x,self.player.y
    def load_sounds(self):
        for i,j in gameconst.sounds.items():
            name = i
            file = j["file"]
            sample = pygame.mixer.Sound(os.path.join("sounds",file))
            if(sample!=None):
                self.sounds.update({name:{"file":sample,"id":j["id"]}})

    def vanish_all_objects(self):
        for o in self.groups:
            o.state = gameconst.VANISH
    def play_sound(self,name):
        id = 0
        if name in self.sounds:
            ch = pygame.mixer.Channel(self.sounds[name]["id"])
            ch.play(self.sounds[name]["file"])
    def addObject(self,x,y,xspeed,yspeed,life_span,size=1,color=0xffffff,owner=None):

        if(owner=="plyer"):
          obj = plyerbullet(x,y,xspeed,yspeed,life_span,size,color,owner)
        elif owner == "foe":
          obj = foebullet(x,y,xspeed,yspeed,life_span,size,color,owner)
        else:
          obj = obu(x,y,xspeed,yspeed,life_span,size,color,owner)
        self.objects.append(obj)
    def addGroup(self,group):
        self.groups.append(group)
        group.oh = self
        for o in group.objects:
            o.master = group
            self.objects.append(o)
    
    def check_collision(self,x,y,size,obtype):
        for o in self.objects:
            if isinstance(o,obtype):
                dx = x - o.x
                dy = y - o.y
                if (abs(dx) < size) and (abs(dy) < size):
                    o.state = gameconst.DEAD
                    return True
        return False
    def foe_dies(self):
        self.dead_foes += 1
    def player_dies(self):
        pass
    def update(self,screen):
        for o in self.groups:
            o.update()

        for o in self.objects:
            o.update()
            o.render(screen)

        # Do "Garbage collection"
        del_list=[]
        for o in self.objects:
            if o.state == gameconst.DEAD:
                del_list.append(o)

        for o in del_list:
            self.objects.remove(o)

        del_list=[]
        for o in self.groups:
            if o.state == gameconst.DEAD:
                del_list.append(o)

        for o in del_list:
            self.groups.remove(o)
            
class obuGroup(object):
    def __init__(self,data, x, y, xspeed, yspeed,life_span):
        self.objects = []
        self.x = x
        self.y = y
        self.oh = None
        self.xspeed = xspeed
        self.yspeed = yspeed
        self.state = gameconst.ALIVE
        self.object_w = data["w"]
        self.object_h = data["h"]
        self.object_data = data["data"]
        self.block_size = data["block_size"]
        self.myid = uuid.uuid4().hex
        self.color = data["color"]
        yoff = -(self.object_h / 2) * self.block_size 
        for i in range(self.object_h):
            xoff = -(self.object_w / 2) * self.block_size
            for j in range(self.object_w):
                offset = i * self.object_w + j
                if self.object_data[offset] != 0:
                   color = gameconst.palette[self.object_data[offset]]
                   o = obu(x+xoff,y+yoff,xspeed,yspeed,life_span,self.block_size,color,self.myid)
                   self.objects.append(o)
                xoff += self.block_size
            yoff += self.block_size
    
    
    def update(self):
        if self.state == gameconst.DEAD:
            for o in self.objects: #send (blow up) die to all objects forming this entity
                o.die_by_blowup() 
                chan = self.oh.play_sound("EXPLOSION")
                self.objects=[]
        elif self.state == gameconst.VANISH:
            for o in self.objects: #send die to all objects forming this entity
                o.die_now() 
                self.objects=[]

    def set_pos(self,dx,dy):
        self.x += dx
        self.y += dy
        for o in self.objects:
            o.x += dx
            o.y += dy

class foe(obuGroup):
    def __init__(self,data, x, y, xspeed, yspeed,life_span):
        super().__init__(data, x, y, xspeed, yspeed,life_span)
        self.fire_counter = 0
        self.attack_mode = gameconst.FOE_NORMAL
    def update(self):
        if self.state == gameconst.DEAD or self.state ==gameconst.VANISH:
            super().update()
            return
        self.x += self.xspeed
        ydelta = 0
        if(self.x > gameconst.SCREEN_W or self.x < 0):
            self.xspeed = -self.xspeed
            self.y += 48
            ydelta = 48
        for i in range(len(self.objects)):
            obj = self.objects[i]
            obj.xspeed = self.xspeed
            obj.y += ydelta
        res = False
        if self.oh != None:
          res = self.oh.check_collision(self.x,self.y,self.object_w*self.block_size,plyerbullet)
        if res == True:
            self.oh.foe_dies()
            self.state = gameconst.DEAD
            self.oh.get_player().update_score(gameconst.FOE_BASE_SCORE)
        # firing
        self.fire_counter+=1
        if self.fire_counter > (gameconst.FOE_FIRE_DELAY / self.oh.level): # TODO make level specific
            px,py = self.oh.get_player_pos()
            if(random.random()*100) < 2:
                if abs(self.x - px) < 80:
                    self.oh.addObject(self.x,self.y - self.block_size*self.object_h,0,8,gameconst.MISSILE_LIFE,8,0xffffaa,"foe")
                    self.oh.play_sound("FOE_GUN")
                self.fire_counter = 0

        super().update()

class saucer(obuGroup):
    def __init__(self,data, x, y, xspeed, yspeed,life_span):
        super().__init__(data, x, y, xspeed, yspeed,life_span)
    def update(self):
        if self.state == gameconst.DEAD:
            return
        self.x += self.xspeed
        self.y += self.yspeed
        res = False
        if self.oh != None:
          res = self.oh.check_collision(self.x,self.y,self.object_w*self.block_size,plyerbullet)
        if res == True:
            self.state = gameconst.DEAD
        super().update()

class player(obuGroup):
    def __init__(self,data, x, y, xspeed, yspeed,life_span):
        super().__init__(data, x, y, xspeed, yspeed,life_span)
        self.score = 0
    def update_score(self,points):
        self.score += points
    def update(self):
        res = self.oh.check_collision(self.x,self.y,self.object_w*self.block_size,foebullet)
        if res == True:
            self.oh.player_dies()
            self.state = gameconst.DEAD
        super().update()
    def move(self,keys,fire_counter,dt):
        deltax = 0
        deltay = 0
        '''
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            deltay = -300 * dt
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            deltay += 300 * dt
        '''
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            deltax = -300 * dt
            if self.x + deltax < 0:
                deltax = 0
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            deltax = 300 * dt
            if self.x + deltax > gameconst.SCREEN_W:
                deltax = 0
        self.set_pos(deltax,deltay)
        # Fire a poro jectile
        if keys[pygame.K_SPACE]:
            if fire_counter > gameconst.FIRE_DELAY:
                self.oh.addObject(self.x,self.y - self.block_size*self.object_h,0,-8,gameconst.MISSILE_LIFE,4,0xffffaa,"plyer")
                fire_counter = 0
                self.oh.play_sound("GUN")
        return fire_counter
#######################################################################
#   O B J E C T S
########################################################################
class obu(object):
    def __init__(self,x,y,xspeed,yspeed,life_span,size=1,color = 0xffffff,owner=None,oh=None):
        self.oh = oh
        self.x = x
        self.y = y
        self.state = gameconst.ALIVE
        self.life_span = life_span
        self.xspeed = xspeed
        self.yspeed = yspeed
        self.color = color
        self.size = size
        self.owner = owner
        self.dieCounter = 0
    def die_by_blowup(self):
        self.xspeed = (random.random()-0.5)*5
        self.yspeed = (random.random()-0.5)*5
        self.color = (random.random()*127+127,random.random()*127+127,random.random()*127)
        self.die()
    def die(self):
        self.state = gameconst.DYING
    def die_now(self):
        self.state = gameconst.DEAD
    def update(self):
        if self.state == gameconst.DYING:
            self.dieCounter+=1
            if self.dieCounter > 100:
                self.state = gameconst.DEAD     
        if self.state == gameconst.DEAD:
            return
        if self.life_span > 0:
          self.life_span -= 1
        if self.life_span == 0:
            self.state = gameconst.DEAD
        
        self.x += self.xspeed
        self.y += self.yspeed
    
    def render(self,screen):
        if self.state == gameconst.DEAD:
            return
        pygame.draw.rect(screen,self.color,(self.x,self.y,self.size,self.size))

class plyerbullet(obu):
        def __init__(self,x,y,xspeed,yspeed,life_span,size=1,color = 0xffffff,owner=None,oh=None):
            super().__init__(x,y,xspeed,yspeed,life_span,size,color,owner,oh)

class foebullet(obu):
        def __init__(self,x,y,xspeed,yspeed,life_span,size=1,color = 0xffffff,owner=None,oh=None):
            super().__init__(x,y,xspeed,yspeed,life_span,size,color,owner,oh)
