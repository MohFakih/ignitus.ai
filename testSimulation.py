from simulation.Basic2DSim import World
from utils.Serialization import load_world_from_file, encode
import numpy as np
import pygame, sys

filename = "worlds/editorTest.world"
world = load_world_from_file(filename)

pygame.init()

size = width, height = 320, 320
block_width = width/world.W
block_height= height/world.H
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Fire Simulation') 
font = pygame.font.Font('freesansbold.ttf', 32)
timestep = 0
display_mode = 0
DISPLAY_MODES = 3
clock = pygame.time.Clock()
textTimer = 255
displayText = "Simulation"
text = font.render(displayText, True, (textTimer,textTimer,textTimer))
textRect = text.get_rect()  
textRect.center = (width//2, height//2)
d = {}
d[0] = "Simulation"
d[1] = "Flammable"
d[2] = "Heatmap"
while 1:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            ky = pygame.key.get_pressed()
            if ky[pygame.K_r]:
                timestep += 1
                world.step()
            if ky[pygame.K_d]:
                textTimer = 255
                display_mode = (display_mode+1)%DISPLAY_MODES
                displayText = d[display_mode]
            if ky[pygame.K_s]:
                pygame.image.save(screen, "sc"+str(timestep)+".png")

    screen.fill((0, 0, 0))
    if display_mode == 0:
        world.draw(screen, block_width, block_height)
    elif display_mode == 1:
        world.draw(screen, block_width, block_height, 'adjacentFlammable')
    elif display_mode == 2:
        world.draw(screen, block_width, block_height, 'vicinityFlameCount')

    textTimer = max(0, textTimer-3)
    if textTimer > 80:
        text = font.render(displayText, True, (textTimer,textTimer,textTimer))
        screen.blit(text, textRect) 
    pygame.display.flip()