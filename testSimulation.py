from Basic2DSim import World, prettyGrid
import pygame, sys

filename = "testFireSpread.world"
world = World(0, 0)
world.load_world_from_file(filename)

pygame.init()

size = width, height = 320, 320
block_width = width/world.W
block_height= height/world.H
screen = pygame.display.set_mode(size)
timestep = 0
display_mode = 0
DISPLAY_MODES = 3
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            ky = pygame.key.get_pressed()
            if ky[pygame.K_r]:
                timestep += 1
                world.step()
            if ky[pygame.K_d]:
                display_mode = (display_mode+1)%DISPLAY_MODES

    screen.fill((0, 0, 0))
    if display_mode == 0:
        world.draw(screen, block_width, block_height)
    elif display_mode == 1:
        world.draw(screen, block_width, block_height, 'adjacentFlammable')
    elif display_mode == 2:
        world.draw(screen, block_width, block_height, 'vicinityFlameCount')

    pygame.display.flip()