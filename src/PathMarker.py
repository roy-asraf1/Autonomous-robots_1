import pygame

class PathMarker:
    def __init__(self, radius, color):
        self.radius = radius
        self.color = color
        self.positions = []

    def add_position(self, position):
        self.positions.append(position)

    def draw(self, window):
        for position in self.positions:
            pygame.draw.circle(window, self.color, position, self.radius)

    def clear_positions(self):
        self.positions = []
