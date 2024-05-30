import pygame
import sys
from pygame.locals import *
from threading import Thread
import time

# Assuming the existence of these classes based on your Java code
from AutoAlgo1_full import AutoAlgo1  # Your AI algorithm
import CPU  # Your CPU class for managing threading and processes

class Button:
    def __init__(self, x, y, width, height, text, callback):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback
        self.font = pygame.font.SysFont(None, 36)

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        screen.blit(text_surface, (self.rect.x + 5, self.rect.y + 10))

    def handle_event(self, event):
        if event.type == MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.callback()

class SimulationWindow:
    def __init__(self, map_image):
        pygame.init()
        self.screen = pygame.display.set_mode((1800, 700), pygame.RESIZABLE)
        pygame.display.set_caption('Drone Simulator')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 36)
        self.map_image = pygame.image.load(map_image)
        self.return_home = False
        self.toggleStop = True
        self.toggleRealMap = True
        self.toggleAI = False
        # self.algo1 = AutoAlgo1()

        self.create_buttons()
        self.run()

    def create_buttons(self):
        self.buttons = [
            Button(1600, 0, 170, 50, 'Start/Pause', self.toggle_start_pause),
            
            # Button(1300, 100, 100, 50, 'speedUp', self.algo1.speed_up),
            # Button(1400, 100, 50, 50, 'speedDown', self.algo1.speed_down),
            # Add more buttons here...
        ]

    def toggle_start_pause(self):
        if self.toggleStop:
            CPU.stopAllCPUS()
        else:
            CPU.resumeAllCPUS()
        self.toggleStop = not self.toggleStop

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                for button in self.buttons:
                    button.handle_event(event)

            self.screen.blit(self.map_image, (0, 0))
            for button in self.buttons:
                button.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(60)

if __name__ == '__main__':
    app = SimulationWindow('Maps/p12.png')
    app.run()
