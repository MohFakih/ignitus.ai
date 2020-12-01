from simulation.Basic2DSim import World
from utils.Serialization import serialize
import pygame, sys

filename = "worlds/testFireSpread.world"
world = World(20, 20)

pygame.init()

size = width, height = 320, 320
block_width = width/world.W
block_height= height/world.H
screen = pygame.display.set_mode(size)

timestep = 0
editor_block = 0
EDITOR_BLOCKS = 4


pygame.display.set_caption('World Editor') 
font = pygame.font.Font('freesansbold.ttf', 32)
clock = pygame.time.Clock()
textTimer = 255
displayText = "wood"
text = font.render(displayText, True, (textTimer,textTimer,textTimer))
textRect = text.get_rect()  
textRect.center = (width//2, height//2)
d = {}
d[0] = "wood"
d[1] = "fire"
d[2] = "air"
d[3] = "victim"
while 1:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            ky = pygame.key.get_pressed()
            if ky[pygame.K_d]:
                textTimer = 255
                editor_block = (editor_block+1)%EDITOR_BLOCKS
                displayText = d[editor_block]
            if ky[pygame.K_s]:
                worldStr = serialize(world)
                worldFile = open("worlds/editorTest.world", 'w')
                worldFile.write(worldStr)

    screen.fill((0, 0, 0))
    if pygame.mouse.get_pressed()[0] == 1:
        x, y = pygame.mouse.get_pos()
        xoords = (int(y//block_width), int(x//block_height))
        world.createCell(xoords, d[editor_block])
    world.draw(screen, block_width, block_height)
    textTimer = max(0, textTimer-3)
    if textTimer > 80:
        text = font.render(displayText, True, (textTimer,textTimer,textTimer))
        screen.blit(text, textRect) 
    pygame.display.flip()