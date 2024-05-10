import pygame
import sys
import os

'''Variables'''
ALPHA = (0,0,0)
BACKGROUND = (218,155,155)
SCALE = 3

worldx = (240)*SCALE
worldy = (180)*SCALE
fps = 30

'''Objects''' # Classes and functions
def init_images(dir):
   l1,l2=[],[]
   for i in os.listdir(f'.\\images\\{dir}\\'): # Save every image into memory
      img = pygame.image.load(os.path.join('images', f'{dir}\\{i}'))
      img = pygame.transform.scale(img, (img.get_width()*SCALE,img.get_height()*SCALE)).convert()
      img.convert_alpha()
      img.set_colorkey(ALPHA)
      l1.append(img)
      l2.append(i)
   return (l1,l2)
class Player(pygame.sprite.Sprite):
   def __init__(self):
      pygame.sprite.Sprite.__init__(self)
      self.frame = 0 # count frames
      self.speed = 2*SCALE # player speed
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
      if not (self.rect.left>=0 and self.rect.right<=worldx): self.rect.x -= h * self.speed
      if not (self.rect.top>=0 and self.rect.bottom<=worldy): self.rect.y -= v * self.speed
   def update(self):
      keys = pygame.key.get_pressed()
      h,v=(keys[pygame.K_d] - keys[pygame.K_a]),(keys[pygame.K_s] - keys[pygame.K_w])
      if keys[pygame.K_SPACE]: bullets.append(Bullet(self.rect.x+((31+(h*2))*SCALE),self.rect.y+((22+h+v)*SCALE)))
      self.hitbox = (self.rect.x + (15*SCALE), self.rect.y + (17*SCALE), 6*SCALE, 6*SCALE)
      self.rect.x += h * self.speed
      self.rect.y += v * self.speed
      self.set_frame(h,v)
      self.collision(h,v)
class Bullet(object):
   def __init__(self,x,y):
      self.speed = 13
      self.x = x
      self.y = y
      self.images,self.imageref=init_images("bullet")[0],init_images("bullet")[1]
   def update(self,world):
      self.image=self.images[0]
      world.blit(self.image,(self.x,self.y))
'''Setup'''
pygame.init()
pygame.display.set_caption("BunBun's Delivery")
pygame.display.set_icon(pygame.image.load(r'.\images\favicon.ico'))
world = pygame.display.set_mode([worldx, worldy])
clock = pygame.time.Clock() 

#player
player = Player()
player.rect.x,player.rect.y = (6)*SCALE,(6)*SCALE # starting position
player_group = pygame.sprite.Group()
player_group.add(player)

def draw_game():
   world.fill(BACKGROUND)
   player.update()
   player_group.draw(world)
   # pygame.draw.rect(world,(255,0,0),player.hitbox)
   for bullet in bullets:
      bullet.update(world)
   pygame.display.flip()

'''Main Loop'''
bullets=[]
while True: 
   clock.tick(fps)
   for event in pygame.event.get():
      if event.type == pygame.QUIT: pygame.quit(); sys.exit()
   for bullet in bullets:
      if bullet.x < worldx and bullet.x > 0:
         bullet.x += bullet.speed*SCALE
      else:
         bullets.pop(bullets.index(bullet))
   draw_game()