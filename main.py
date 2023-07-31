import pygame
import random
import os
import d_types
import d_map
import time

WIDTH = 32*26
HEIGHT = 1080//2
FPS = 60

# Define Colors 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

## initialize pygame and create window
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wand Editor")
clock = pygame.time.Clock()     ## For syncing the FPS
box = pygame.transform.scale(pygame.image.load("ui/inventory_box.png").convert_alpha(),(32,32))
spell_info = []
translations = d_map.get_info()
enum = ["projectile","static_projectile","modifier","draw_many","material","other","utility","passive"]
for spell in d_types.get_info():
  #print(spell[0][1:])
  try:
    spell_info.append((
      translations[spell[0][1:]],
      enum[spell[1]],
      pygame.transform.scale(pygame.image.load("spells/"+spell[2].split("/")[-1]).convert_alpha(),(32,32)),
      spell[3]
    ))
  except:
    spell_info.append((
      "???",
      enum[spell[1]],
      pygame.transform.scale(pygame.image.load("spells/"+spell[2].split("/")[-1]).convert_alpha(),(32,32)),
      spell[3]
    ))
    print(spell[0][1:])

def name_to_id(name):
  for k,v in enumerate(spell_info):
    if v[3] == name:
      return k

## group all the sprites together for ease of update
def tick():
  pass

spells = ["DAMAGE","LUMINOUS_DRILL"]

def render():
  for i in range(26):
    screen.blit(box,(32*i,0))
  
  for k,spell in enumerate(spells):
    screen.blit(spell_info[name_to_id(spell)][2],(32*k,0))

## Game loop
running = True
while running:
    #1 Process input/events
    clock.tick(FPS)     ## will make the loop run at the same speed all the time
    for event in pygame.event.get():        # gets all the events which have occured till now and keeps tab of them.
        ## listening for the the X button at the top
        if event.type == pygame.QUIT:
            running = False
    #tick
    
    #3 Draw/render
    screen.fill(BLACK)
    render()
    pygame.display.flip()       

pygame.quit()
