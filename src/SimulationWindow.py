import pygame
import sys
import time
from pygame.locals import *
from AutoAlgo1 import AutoAlgo1
from CPU import CPU
from Point import Point
from Map import Map
from Painter import Painter


def show_loading_screen(display):
    font = pygame.font.Font(None, 36)
    text = font.render('Loading...', True, (255, 255, 255))
    text_rect = text.get_rect(center=(display.get_width()//2, display.get_height()//2))
    display.blit(text, text_rect)
    pygame.display.flip()


class SimulationWindow:
    def __init__(self):
        pygame.init()
        info = pygame.display.Info()
        self.screen_width, self.screen_height = info.current_w - 100, info.current_h - 100
        self.frame = pygame.display.set_mode((self.screen_width, self.screen_height), RESIZABLE)
        pygame.display.set_caption("Drone Simulator")

        # Show loading screen
        show_loading_screen(self.frame)

        # Initialize game components here after resources are loaded
        self.map = Map("../Maps/p12.png", Point(100, 50))
        self.algo1 = AutoAlgo1(self.map)
        self.painter = Painter(self.algo1)
        self.running = True
        self.toggle_stop = True
        self.toggle_real_map = True
        self.toggle_ai = False
        self.return_home = False
        self.init_ui()

    def init_ui(self):
        # Define buttons within the 25% right part of the screen
        buttons_area_start = self.screen_width * 0.75
        button_width = 100  # Smaller width
        button_height = 40  # Smaller height
        button_spacing = 10  # Spacing between buttons
        first_column_x = buttons_area_start + 20  # X position for the first column
        second_column_x = first_column_x + button_width + button_spacing  # X position for the second column

        # Y starting position for the buttons
        starting_y = 20
        y_increment = button_height + 10  # Space between buttons vertically

        # Buttons configuration
        self.buttons = {
            'Stop/Resume': (pygame.Rect(first_column_x, starting_y, button_width, button_height), self.handle_stop_resume),
            'Speed Up': (pygame.Rect(second_column_x, starting_y, button_width, button_height), self.handle_speed_up),
            'Slow Down': (pygame.Rect(first_column_x, starting_y + y_increment, button_width, button_height), self.handle_slow_down),
            'Spin 180': (pygame.Rect(second_column_x, starting_y + y_increment, button_width, button_height), lambda: self.handle_spin(180)),
            'Spin 90': (pygame.Rect(first_column_x, starting_y + 2 * y_increment, button_width, button_height), lambda: self.handle_spin(90)),
            'Spin 60': (pygame.Rect(second_column_x, starting_y + 2 * y_increment, button_width, button_height), lambda: self.handle_spin(60)),
            'Spin 45': (pygame.Rect(first_column_x, starting_y + 3 * y_increment, button_width, button_height), lambda: self.handle_spin(45)),
            'Spin 30': (pygame.Rect(second_column_x, starting_y + 3 * y_increment, button_width, button_height), lambda: self.handle_spin(30)),
            'Spin -30': (pygame.Rect(first_column_x, starting_y + 4 * y_increment, button_width, button_height), lambda: self.handle_spin(-30)),
            'Spin -45': (pygame.Rect(second_column_x, starting_y + 4 * y_increment, button_width, button_height), lambda: self.handle_spin(-45)),
            'Toggle AI': (pygame.Rect(first_column_x, starting_y + 5 * y_increment, button_width, button_height), self.handle_toggle_ai),
            'Return Home': (pygame.Rect(second_column_x, starting_y + 5 * y_increment, button_width, button_height), self.handle_return_home),
        }
        self.font = pygame.font.Font(None, 22)  # Smaller font size for smaller buttons

    def main_loop(self):
        while self.running:
            self.frame.fill((0, 0, 0))  # Clear the screen with black before drawing
            self.map.paint(self.frame)  # Draw the map on 75% of the screen

            # Handle events and draw buttons
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == VIDEORESIZE:
                    self.screen_width, self.screen_height = event.w, event.h
                    self.frame = pygame.display.set_mode((self.screen_width, self.screen_height), RESIZABLE)
                    self.init_ui()
                elif event.type == MOUSEBUTTONDOWN:
                    for button_text, (rect, action) in self.buttons.items():
                        if rect.collidepoint(event.pos):
                            action()

            # Draw buttons with text
            for text, (rect, _) in self.buttons.items():
                pygame.draw.rect(self.frame, (200, 200, 200), rect)
                self.frame.blit(self.font.render(text, True, (0, 0, 0)), (rect.x + 5, rect.y + 10))

            pygame.display.flip()
            time.sleep(0.016)  # Maintain frame rate

    def handle_stop_resume(self):
        self.toggle_stop = not self.toggle_stop
        if self.toggle_stop:
            CPU.resume_all_cpus()
        else:
            CPU.stop_all_cpus()

    def handle_speed_up(self):
        self.algo1.speed_up()

    def handle_slow_down(self):
        self.algo1.speed_down()

    def handle_spin(self, degrees):
        self.algo1.spin_by(degrees)

    def handle_toggle_map(self):
        self.toggle_real_map = not self.toggle_real_map

    def handle_toggle_ai(self):
        self.toggle_ai = not self.toggle_ai

    def handle_return_home(self):
        self.return_home = not self.return_home
        self.algo1.return_home()

if __name__ == "__main__":
    app = SimulationWindow()
    app.main_loop()
