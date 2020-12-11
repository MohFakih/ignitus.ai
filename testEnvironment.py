from RLTests.singleAgent import SingleAgentEnvironment
from utils.Serialization import load_world_from_file, encode
import numpy as np
import pygame, sys

filename = "worlds/editorTest.world"
agent = SingleAgentEnvironment(filename)
world = agent.world
pygame.init()

size = width, height = 320, 320
block_width = width/world.W
block_height= height/world.H
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Agent Test')
timestep = 0
clock = pygame.time.Clock()
action = 0

observation = agent.reset()
while 1:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            ky = pygame.key.get_pressed()
            if ky[pygame.K_r]:
                timestep += 1
                observation, reward, temrinal = agent.step(action)
                action = 0
            if ky[pygame.K_w]:
                action = 1
            elif ky[pygame.K_d]:
                action=2
            elif ky[pygame.K_s]:
                action=3
            elif ky[pygame.K_a]:
                action=4
            elif ky[pygame.K_SPACE]:
                action = 5
            elif ky[pygame.K_TAB]:
                action = 6
            elif ky[pygame.K_LSHIFT]:
                action = 7

                

    screen.fill((0, 0, 0))

    agent.world.draw(screen, block_width, block_height)
    
    pygame.draw.rect(screen, (255, 255, 0), agent.getRect(block_width, block_height))

    pygame.display.flip()