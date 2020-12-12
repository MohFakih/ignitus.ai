import pygame

class pygameWindow:
    def __init__(self, w, h):          
        pygame.init()
        self.size = self.width, self.height = w, h
        self.screen = pygame.display.set_mode(self.size)
    
    def draw(self, agent):
        self.screen.fill((0, 0, 0))
        block_width = self.width/agent.world.W
        block_height= self.height/agent.world.H
        agent.world.draw(self.screen, block_width, block_height)
        pygame.draw.rect(self.screen, (255, 255, 0), agent.getRect(block_width, block_height))
        pygame.display.flip()