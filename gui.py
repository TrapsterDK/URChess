#gui
import pygame

class GUI:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("monospace", 15)
        self.text = self.font.render("Hello World", 1, (255,255,0))
        self.screen.blit(self.text, (10, 10))
        pygame.display.flip()
        self.running = True
        self.clock = pygame.time.Clock() 