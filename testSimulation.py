from Basic2DSim import *
import pygame, sys

filename = "TestFireSpread.world"
world = World(0, 0)
world.load_world_from_file(filename)

pygame.init()

size = width, height = 320, 320
block_width = width/world.W
block_height= height/world.H
BLACK = (0, 0, 0)
RED   = (255, 0, 0)
BROWN = (150, 100, 50)
screen = pygame.display.set_mode(size)
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if pygame.key.get_pressed()[pygame.K_r]:
                world.step()

    screen.fill(BLACK)
    for cell in world.list_cells():
        rect = [cell.x * block_width, cell.y * block_height, block_width, block_height]
        block_type = cell.block.block_type
        if block_type == 'air':
            pygame.draw.rect(screen, BLACK, rect)
        elif block_type == 'wood':
            pygame.draw.rect(screen, BROWN, rect)
        elif block_type == 'fire':
            pygame.draw.rect(screen, RED, rect)

    pygame.display.flip()