import pygame
import sys

class Graph:
    def __init__(self):
        self.g = {}
        self.vertices = []

    def add_vertex(self, name):
        if name not in self.g:
            self.g[name] = []
            self.vertices.append(name)
            if len(self.vertices) > 1:
                last_vertex = self.vertices[-2]
                self.add_edge(last_vertex, name)

    def add_edge(self, v1, v2):
        if v1 in self.g:
            self.g[v1].append(v2)
        if v2 not in self.g:
            self.g[v2] = []

    def get_graph(self):
        return self.g

    def draw_graph(self, screen, positions):
        # Draw each vertex
        for vertex in positions:
            pygame.draw.circle(screen, (0, 255, 0), positions[vertex], 5)
            if vertex in self.g:
                for neighbor in self.g[vertex]:
                    if neighbor in positions:
                        pygame.draw.line(screen, (255, 0, 0), positions[vertex], positions[neighbor], 2)
