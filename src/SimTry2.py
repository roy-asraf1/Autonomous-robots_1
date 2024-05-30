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
        # Drawing the button background with a white color
        pygame.draw.rect(screen, (255, 255, 255), self.rect)  # White background
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)  # Black border to make it stand out
        text_surface = self.font.render(self.text, True, (0, 0, 0))  # Black text
        # Centering text in the button
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

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
            # Button(1400, 100, 100, 50, 'speedDown', self.algo1.speed_down),
            # Button(1300, 200, 100, 50, 'spin180', lambda: self.algo1.spin_by(180)),
            # Button(1400, 200, 100, 50, 'spin90', lambda: self.algo1.spin_by(90)),
            # Button(1500, 200, 100, 50, 'spin60', lambda: self.algo1.spin_by(60)),
            # Button(1300, 300, 100, 50, 'spin45', lambda: self.algo1.spin_by(45)),
            # Button(1400, 300, 100, 50, 'spin30', lambda: self.algo1.spin_by(30)),
            # Button(1500, 300, 100, 50, 'spin-30', lambda: self.algo1.spin_by(-30)),
            # Button(1600, 300, 100, 50, 'spin-45', lambda: self.algo1.spin_by(-45)),
            # Button(1700, 300, 100, 50, 'spin-60', lambda: self.algo1.spin_by(-60)),
            Button(1600, 300, 150, 50, 'toggle Map', self.toggle_map),
            Button(1650, 350, 150, 50, 'toggle AI', self.toggle_ai),
            # Button(1500, 400, 120, 50, 'Return Home', self.return_home_func),
            # Button(1600, 400, 120, 50, 'Open Graph', self.open_graph),
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
                elif event.type == MOUSEBUTTONDOWN:
                    for button in self.buttons:
                        if button.rect.collidepoint(event.pos):
                            button.callback()

            self.screen.blit(self.map_image, (0, 0))
            for button in self.buttons:
                button.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(60)
    
    def toggle_map(self):
        self.toggleRealMap = not self.toggleRealMap

    def toggle_ai(self):
        self.toggleAI = not self.toggleAI

    # def return_home_func(self):
    #     self.return_home = not self.return_home
    #     self.algo1.speed_down()
    #     self.algo1.spin_by(180, True, self.algo1.speed_up)

    # def open_graph(self):
    #     self.algo1.m_graph.draw_graph()


if __name__ == '__main__':
    app = SimulationWindow('Maps/p12.png')
    app.run()
