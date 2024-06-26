import pygame
import sys
import os

def s(var): return var*SCALE

'''Variables'''
ALPHA = (0,0,0)
BACKGROUND = (218,155,155)
SCALE = 3  

worldx = s(240)
worldy = s(180)
fps = 30

'''Objects''' # Classes and functions
def init_images(dir,folder=True):
   l1,l2=[],[]
   truedir=f'.\\images\\{dir}\\' if folder else f'.\\images\\{dir}'
   for i in os.listdir(truedir): # Save every image into memory
      if os.path.exists(truedir+i):
         img = pygame.image.load(truedir+i)
         img = pygame.transform.scale(img, (s(img.get_width()),s(img.get_height()))).convert()
         img.convert_alpha()
         img.set_colorkey(ALPHA)
         l1.append(img)
         l2.append(i)
   return (l1,l2)
class Player(pygame.sprite.Sprite):
   def __init__(self):
      pygame.sprite.Sprite.__init__(self)
      self.frame = 0 # count frames
      self.speed = s(2) # player speed
      self.last_shot = pygame.time.get_ticks()
      self.images,self.imageref = init_images("bunbun")[0],init_images("bunbun")[1]
      self.image = self.images[self.imageref.index("idle.png")]
      self.rect = self.image.get_rect()
   def set_frame(self,h,v):
      if h<0: self.image=self.images[self.imageref.index("left.png")]
      elif h>0: self.image=self.images[self.imageref.index("right.png")]
      elif v<0: self.image=self.images[self.imageref.index("up.png")]
      elif v>0: self.image=self.images[self.imageref.index("down.png")]
      else: self.image=self.images[self.imageref.index("idle.png")]
   def collision(self,h,v):
      if not (self.rect.left>=(0) and self.rect.right<=worldx): self.rect.x -= h * self.speed
      if not (self.rect.top>=s(0) and self.rect.bottom<=worldy): self.rect.y -= v * self.speed
   def update(self):
      keys = pygame.key.get_pressed()
      h,v=(keys[pygame.K_d] - keys[pygame.K_a]),(keys[pygame.K_s] - keys[pygame.K_w])
      time_now = pygame.time.get_ticks()
      if keys[pygame.K_SPACE] and time_now - self.last_shot > 60: 
         bulletx=self.rect.x+s(31+(h*2))
         bullety=self.rect.y+s(22+h+v)
         bullets.append(Bullet(bulletx,bullety))
         fx.append(Effect(bulletx-s(1),bullety-s(2),"fx\\pew",2))
         self.last_shot = time_now
      self.hitbox = (self.rect.x + s(15), self.rect.y + s(17), s(6), s(6))
      self.rect.x += h * self.speed
      self.rect.y += v * self.speed
      self.set_frame(h,v)
      self.collision(h,v)
class Bullet(object):
   def __init__(self,x,y):
      self.speed = s(5)
      self.x,self.y = x,y
      self.images,self.imageref=init_images("bullet")[0],init_images("bullet")[1]
   def update(self,world):
      self.image=self.images[0]
      world.blit(self.image,(self.x,self.y))
class Effect(object):
   def __init__(self,x,y,dir,len=0):
      self.x,self.y,self.len=x,y,len
      self.images=init_images(dir)[0]
      self.imageref=init_images(dir)[1]
   def update(self,world):
      for i in range(self.len):
         world.blit(self.images[i],(self.x,self.y))
      fx.remove(fx[-1])
'''Setup'''
pygame.init()
pygame.display.set_caption("BunBun's Delivery")
pygame.display.set_icon(pygame.image.load(r'.\images\favicon.ico'))
world = pygame.display.set_mode([worldx, worldy])
clock = pygame.time.Clock() 

#player
player = Player()
player.rect.x,player.rect.y = s(6),s(6) # starting position
player_group = pygame.sprite.Group()
player_group.add(player)

def draw_game():
   world.fill(BACKGROUND)
   player.update()
   player_group.draw(world)
   # pygame.draw.rect(world,(255,0,0),player.hitbox)
   for bullet in bullets: bullet.update(world)
   for effect in fx: effect.update(world)
   pygame.display.flip()

'''Main Loop'''
bullets=[]
fx=[]
while True: 
   clock.tick(fps)
   for event in pygame.event.get():
      if event.type == pygame.QUIT: pygame.quit(); sys.exit()
   for bullet in bullets:
      if bullet.x < worldx and bullet.x > 0:
         bullet.x += s(bullet.speed)
      else:
         bullets.pop(bullets.index(bullet))
   draw_game()