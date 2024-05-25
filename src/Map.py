import pygame

class Map:
    def __init__(self, map_image_path, screen_width, screen_height):
        self.map_image = pygame.image.load(map_image_path)
        self.map_image = pygame.transform.scale(self.map_image, (screen_width, screen_height))
        self.screen_width = screen_width
        self.screen_height = screen_height

    def is_walkable(self, x, y):
        if not self._is_within_bounds(x, y):
            return False
        return self._is_white_pixel(x, y)

    def _is_within_bounds(self, x, y):
        return 0 <= x < self.screen_width and 0 <= y < self.screen_height

    def _is_white_pixel(self, x, y):
        pixel_color = self.map_image.get_at((int(x), int(y)))
        return pixel_color == (255, 255, 255, 255)  # Check for white color

    def get_pixel_color(self, x, y):
        if self._is_within_bounds(x, y):
            return self.map_image.get_at((int(x), int(y)))
        return None

    def find_nearest_walkable(self, start_x, start_y):
        # Example of a naive search algorithm to find the nearest walkable position
        for radius in range(1, max(self.screen_width, self.screen_height)):
            for dx in range(-radius, radius + 1):
                for dy in range(-radius, radius + 1):
                    new_x, new_y = start_x + dx, start_y + dy
                    if self.is_walkable(new_x, new_y):
                        return new_x, new_y
        return start_x, start_y

    def count_walkable_pixels(self):
        count = 0
        for y in range(self.screen_height):
            for x in range(self.screen_width):
                if self.is_walkable(x, y):
                    count += 1
        return count
