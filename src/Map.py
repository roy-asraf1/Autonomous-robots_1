import pygame
from Point import Point

class Map:
    def __init__(self, path, drone_start_point):
        self.drone_start_point = drone_start_point
        self.map_image = self.load_map(path)
        self.scaled_map_image = None  # This will hold the scaled image

    def load_map(self, path):
        # Load the image using Pygame, and handle potential errors
        try:
            image = pygame.image.load(path)
            return image
        except pygame.error as e:
            print(f"Failed to load the map image from {path}: {e}")
            return None

    def paint(self, surface):
        if self.map_image:
            if not self.scaled_map_image or self.scaled_map_image.get_size() != surface.get_size():
                try:
                    map_width = int(surface.get_width() * 0.75)  # 75% of the screen width
                    map_height = surface.get_height()
                    self.scaled_map_image = pygame.transform.scale(self.map_image, (map_width, map_height))
                except Exception as e:
                    print(f"Failed to scale map image: {e}")
                    self.scaled_map_image = None
            if self.scaled_map_image:
                surface.blit(self.scaled_map_image, (0, 0))
            else:
                print("Scaled map image is not available.")
        else:
            print("Map image not loaded, cannot paint.")


    def is_collide(self, x, y):
        if 0 <= x < self.map_image.get_width() and 0 <= y < self.map_image.get_height():
            color = self.map_image.get_at((x, y))
            return color != pygame.Color(255, 255, 255, 255)
        return True