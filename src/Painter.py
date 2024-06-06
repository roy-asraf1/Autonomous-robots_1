import pygame

class Painter:
    def __init__(self, algo):
        self.algo = algo

    def paint(self, surface):
        self.algo.paint(surface)
