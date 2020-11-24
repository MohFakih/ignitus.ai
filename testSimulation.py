from Basic2DSim import *
import pygame, sys

filename = "TestFireSpread.world"
world = World(0, 0)
world.load_world_from_file(filename)

pygame.init()

size = width, height = 320, 320
block_width = width/world.W
block_height= height/world.H
screen = pygame.display.set_mode(size)
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if pygame.key.get_pressed()[pygame.K_r]:
                world.step()
                print(str(world))

    screen.fill(BLACK)
    for cell in world.list_cells():
        cell.draw(screen, block_width, block_height)

    pygame.display.flip()