import pygame
import random

class Graph:
    def __init__(self):
        self.vertices = []
        self.edges = []

    def addVertex(self, point):
        if len(self.vertices) > 0:
            last_vertex = self.vertices[-1]
            self.edges.append((last_vertex, point))
        self.vertices.append(point)

    def drawGraph(self, surface):
        for edge in self.edges:
            start_pos = (int(edge[0].x), int(edge[0].y))
            end_pos = (int(edge[1].x), int(edge[1].y))
            pygame.draw.line(surface, (255, 255, 255), start_pos, end_pos)
