import pygame
import pygame_textinput
import random
import os
import d_types
import d_map
import time

WIDTH = 42*26 + 2
HEIGHT = 1080//2
FPS = 240

# Define Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# initialize pygame and create window
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wand Editor")
clock = pygame.time.Clock()  # For syncing the FPS

textinput = pygame_textinput.TextInputVisualizer(font_color=pygame.Color(
    (255, 255, 255)), cursor_color=pygame.Color((255, 255, 255), cursor_width=20))

box = pygame.transform.scale(pygame.image.load(
    "ui/full_inventory_box.png").convert_alpha(), (40, 40))
highlight = pygame.transform.scale(pygame.image.load(
    "ui/item_bg_purchase_1.png").convert_alpha(), (40, 40))
spell_info = []
translations = d_map.get_info()
enum = ["projectile", "static_projectile", "modifier",
        "draw_many", "material", "other", "utility", "passive"]

for spell in d_types.get_info():
    # print(spell[0][1:])
    try:
        spell_info.append((
            translations[spell[0][1:]],
            enum[spell[1]],
            pygame.transform.scale(pygame.image.load(
                "spells/"+spell[2].split("/")[-1]).convert_alpha(), (32, 32)),
            spell[3]
        ))
    except KeyError:
        spell_info.append((
            "???",
            enum[spell[1]],
            pygame.transform.scale(pygame.image.load(
                "spells/"+spell[2].split("/")[-1]).convert_alpha(), (32, 32)),
            spell[3]
        ))
        print(spell[0][1:])


def name_to_id(name):
    for k, v in enumerate(spell_info):
        if v[3] == name:
            return k

# group all the sprites together for ease of update


def tick():
    pass


spells = []
sel = 0


def render():
    x = 0
    y = 2
    for i in range(26):
        screen.blit(box, (42*i+2, 2))
    screen.blit(highlight, (42*sel+2, 2))
    for k, spell_v in enumerate(spells):
        screen.blit(spell_info[name_to_id(spell_v)][2], (42*k+2+4, 2+4))

    screen.blit(textinput.surface, (2, 40))
    for k, spell_v in enumerate(spell_info):
        if textinput.value.lower() in spell_v[0].lower():
            screen.blit(box, (x*42+2, y*42+2))
            screen.blit(spell_info[k][2], (x*42+2+4, y*42+2+4))
            x += 1
            if x >= 26:
                y += 1
                x = 0


# Game loop
running = True
pygame.key.set_repeat(150, 50)  # press every 50 ms after waiting 200 ms
while running:
    clock.tick(FPS)
    events = pygame.event.get()

    for event in events:
        # listening for the the X button at the top
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                pos = pygame.mouse.get_pos()
                pos = ((pos[0]-2)//42, pos[1]//42)  # 2 is spell gui, 1
                if pos[1] >= 2:
                    spell = list(filter(lambda spell: textinput.value.lower(
                    ) in spell[0].lower(), spell_info))[(pos[1]-2)*26+pos[0]]
                    # print(spell[3])
                    spells.insert(sel, spell[3])
                    sel += 1
                elif pos[1] == 0:
                    try:
                        spells.pop(pos[0])
                        if pos[0] <= sel:
                            sel -= 1
                    except IndexError:
                        pass
            elif event.button == 5:
                sel += 1
                sel = min(26, sel)
            elif event.button == 4:
                sel -= 1
                sel = max(0, sel)
            # print(pos)

    textinput.update(events)

    # 3 Draw/render
    screen.fill(BLACK)
    render()
    pygame.display.flip()

pygame.quit()
