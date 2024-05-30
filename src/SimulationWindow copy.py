import pygame
import sys
from pygame.locals import *
from threading import Thread
import time
from CPU import CPU
from Button import  Button
from Drone import  Drone
from AutoAlgo1_full import AutoAlgo1

class SimulationWindow:
    def __init__(self, image_path=None):
        pygame.init()
        self.screen = pygame.display.set_mode((400, 300))
        pygame.display.set_caption('Drone Simulator')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 36)
        self.info_label = ""
        self.info_label2 = ""
        self.return_home = False
        self.toogleStop = True
        self.toogleRealMap = True
        self.toogleAI = False
        # self.algo1 = AutoAlgo1()

        self.create_buttons()

        self.painter_thread = Thread(target=self.run_painter)
        self.painter_thread.start()

        self.updates_thread = Thread(target=self.run_updates)
        self.updates_thread.start()

        self.info_thread = Thread(target=self.run_info)
        self.info_thread.start()

    def create_buttons(self):
        self.buttons = []

        # self.buttons.append(Button(1300, 0, 170, 50, 'Start/Pause', self.toggle_start_pause))
        # self.buttons.append(Button(1300, 100, 100, 50, 'speedUp', self.algo1.speed_up))
        # self.buttons.append(Button(1400, 100, 100, 50, 'speedDown', self.algo1.speed_down))
        # self.buttons.append(Button(1300, 200, 100, 50, 'spin180', lambda: self.algo1.spin_by(180)))
        # self.buttons.append(Button(1400, 200, 100, 50, 'spin90', lambda: self.algo1.spin_by(90)))
        # self.buttons.append(Button(1500, 200, 100, 50, 'spin60', lambda: self.algo1.spin_by(60)))
        # self.buttons.append(Button(1300, 300, 100, 50, 'spin45', lambda: self.algo1.spin_by(45)))
        # self.buttons.append(Button(1400, 300, 100, 50, 'spin30', lambda: self.algo1.spin_by(30)))
        # self.buttons.append(Button(1500, 300, 100, 50, 'spin-30', lambda: self.algo1.spin_by(-30)))
        # self.buttons.append(Button(1600, 300, 100, 50, 'spin-45', lambda: self.algo1.spin_by(-45)))
        # self.buttons.append(Button(1700, 300, 100, 50, 'spin-60', lambda: self.algo1.spin_by(-60)))
        # self.buttons.append(Button(1300, 400, 120, 50, 'toggle Map', self.toggle_map))
        # self.buttons.append(Button(1400, 400, 120, 50, 'toggle AI', self.toggle_ai))
        # self.buttons.append(Button(1500, 400, 120, 50, 'Return Home', self.return_home_func))
        # self.buttons.append(Button(1600, 400, 120, 50, 'Open Graph', self.open_graph))

    def toggle_start_pause(self):
        self.toogleStop = not self.toogleStop
        if self.toogleStop:
            CPU.stopAllCPUS()
        else:
            CPU.resumeAllCPUS()

    def toggle_map(self):
        self.toogleRealMap = not self.toogleRealMap

    def toggle_ai(self):
        self.toogleAI = not self.toogleAI

    def return_home_func(self):
        self.return_home = not self.return_home
        self.algo1.speed_down()
        self.algo1.spin_by(180, True, self.algo1.speed_up)

    def open_graph(self):
        self.algo1.m_graph.draw_graph()

    def run_painter(self):
        while True:
            self.screen.fill((255, 255, 255))
            for button in self.buttons:
                button.draw(self.screen)

            # Call the painter function to draw other components if needed
            self.algo1.paint(self.screen)

            pygame.display.flip()
            self.clock.tick(60)

    def run_updates(self):
        while True:
            self.algo1.drone.update()
            time.sleep(1 / 60)

    def run_info(self):
        while True:
            self.update_info()
            time.sleep(1 / 6)

    def update_info(self):
        self.info_label = self.algo1.drone.get_info_html()
        self.info_label2 = f"Counter: {self.algo1.counter}\nIs Risky: {self.algo1.is_risky}\nRisky Distance: {self.algo1.risky_dis}"

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

            self.screen.fill((255, 255, 255))
            for button in self.buttons:
                button.draw(self.screen)

            info_surface = self.font.render(self.info_label, True, (0, 0, 0))
            self.screen.blit(info_surface, (1300, 500))

            info_surface2 = self.font.render(self.info_label2, True, (0, 0, 0))
            self.screen.blit(info_surface2, (1300, 550))

            pygame.display.flip()
            self.clock.tick(60)


    def toggle_cpu(self):
        CPU.toggle_all_cpus()

    def speed_up(self):
        self.algo.speed_up()

    def speed_down(self):
        self.algo.speed_down()

if __name__ == '__main__':
    input = input('What is the map?\n') # ../Maps/p12.png
    # algo = AutoAlgo1()  # Assuming AutoAlgo1 is properly defined elsewhere
    app = SimulationWindow(input)
    # Load the map image
    map_image = pygame.image.load(app)
    app.run()
