import pygame
import sys
import os

'''Variables'''
ALPHA = (0,0,0)
BACKGROUND = (218,155,155)
SCALE = 2

worldx = (240)*SCALE
worldy = (180)*SCALE
fps = 30

'''Objects''' # Classes and functions
class Player(pygame.sprite.Sprite):
   def __init__(self):
      pygame.sprite.Sprite.__init__(self)
      self.frame = 0 # count frames
      self.speed = 2 # player speed
      self.images = []
      for i in os.listdir(r'.\images\bunbun\\'):
         img = pygame.image.load(os.path.join('images', 'bunbun\\'+i)).convert()
         pygame.transform.scale(img,(SCALE,SCALE)) # Image doesn't get bigger
         img.convert_alpha()
         img.set_colorkey(ALPHA)
         self.images.append(img)
      self.image = self.images[2]
      self.rect = self.image.get_rect()
   def update(self):
      keys = pygame.key.get_pressed()
      h,v=(keys[pygame.K_d] - keys[pygame.K_a]),(keys[pygame.K_s] - keys[pygame.K_w])
      self.hitbox = (self.rect.x + 15, self.rect.y + 17, 6, 6)
      self.rect.x += h * self.speed
      self.rect.y += v * self.speed
      if h<0: self.image=self.images[3]
      elif h>0: self.image=self.images[4]
      elif v<0: self.image=self.images[5]
      elif v>0: self.image=self.images[0]
      else: self.image=self.images[2]
'''Setup'''
pygame.init()
pygame.display.set_caption("Bunbun's Delivery")
pygame.display.set_icon(pygame.image.load(r'.\images\favicon.ico'))
world = pygame.display.set_mode([worldx, worldy])
scaled_world = pygame.transform.scale(world,(2,2))

clock = pygame.time.Clock() 

#player
player = Player()
player.rect.x = 0
player.rect.y = 0
player_group = pygame.sprite.Group()
player_group.add(player)

'''Main Loop'''
while True: 
   for event in pygame.event.get():
      if event.type == pygame.QUIT:
         pygame.quit(); sys.exit()
   world.fill(BACKGROUND)
   player.update()
   player_group.draw(world)
   
   pygame.display.flip()
   clock.tick(fps)