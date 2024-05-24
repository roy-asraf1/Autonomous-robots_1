import pygame
import sys
from pygame.locals import *
from threading import Thread
import threading
import CPU
import Point
import random
import Map
import ProgramingAlgo



class SimulationWindow:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1800, 700))
        pygame.display.set_caption("Drone Simulator")

        self.font = pygame.font.SysFont("Arial", 24)
        self.info_label = ""
        self.info_label2 = ""
        self.toggle_stop = True
        self.running = True

        self.buttons = {
            "start_pause": pygame.Rect(1300, 0, 170, 50),
            "speed_up": pygame.Rect(1300, 100, 100, 50),
            "speed_down": pygame.Rect(1300, 200, 100, 50),
            "graph": pygame.Rect(1600, 400, 120, 50)
        }

        self.init_simulation()
        self.main_loop()

    def init_simulation(self):
        map_num = 4
        start_points = [
            Point(100, 50),
            Point(50, 60),
            Point(73, 68),
            Point(84, 73),
            Point(92, 100)
        ]

        map_path = f"D:/Tests/Maps/p11.png"
        self.map_instance = Map(map_path, start_points[map_num - 1])

        global algo1
        algo1 = ProgramingAlgo(self.map_instance)

        painter_cpu = CPU(200, "painter")
        painter_cpu.add_function(self.update_screen)
        painter_cpu.play()

        algo1.play()

        updates_cpu = CPU(60, "updates")
        updates_cpu.add_function(algo1.drone.update)
        updates_cpu.play()

        info_cpu = CPU(6, "update_info")
        info_cpu.add_function(self.update_info)
        info_cpu.play()

    def main_loop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                elif event.type == MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)

            self.screen.fill((255, 255, 255))
            self.draw_buttons()
            self.draw_info_labels()
            pygame.display.update()

        pygame.quit()
        sys.exit()

    def handle_click(self, pos):
        if self.buttons["start_pause"].collidepoint(pos):
            self.toggle_cpu()
        elif self.buttons["speed_up"].collidepoint(pos):
            algo1.speed_up()
        elif self.buttons["speed_down"].collidepoint(pos):
            algo1.speed_down()
        elif self.buttons["graph"].collidepoint(pos):
            algo1.m_graph.draw_graph()

    def toggle_cpu(self):
        if self.toggle_stop:
            CPU.stop_all_cpus()
        else:
            CPU.resume_all_cpus()
        self.toggle_stop = not self.toggle_stop

    def draw_buttons(self):
        pygame.draw.rect(self.screen, (0, 255, 0), self.buttons["start_pause"])
        self.screen.blit(self.font.render("Start/Pause", True, (0, 0, 0)), (1300, 15))
        
        pygame.draw.rect(self.screen, (0, 0, 255), self.buttons["speed_up"])
        self.screen.blit(self.font.render("Speed Up", True, (255, 255, 255)), (1300, 115))
        
        pygame.draw.rect(self.screen, (0, 0, 255), self.buttons["speed_down"])
        self.screen.blit(self.font.render("Speed Down", True, (255, 255, 255)), (1300, 215))
        
        pygame.draw.rect(self.screen, (128, 0, 128), self.buttons["graph"])
        self.screen.blit(self.font.render("Graph", True, (255, 255, 255)), (1600, 415))

    def draw_info_labels(self):
        self.screen.blit(self.font.render(self.info_label, True, (0, 0, 0)), (1300, 500))
        self.screen.blit(self.font.render(self.info_label2, True, (0, 0, 0)), (1400, 450))

    def update_info(self, delta_time):
        self.info_label = algo1.drone.get_info_html()
        self.info_label2 = f"{algo1.counter} isRisky:{algo1.is_risky} {algo1.risky_dis}"

    def update_screen(self):
        self.screen.fill((255, 255, 255))
        self.map_instance.paint(self.screen)
        for lidar in self.drone.lidars:
            lidar.paint(self.screen)
        pygame.display.flip()

if __name__ == "__main__":
    SimulationWindow()
