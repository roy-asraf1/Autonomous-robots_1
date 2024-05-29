from PIL import Image
import pygame
import Point
import Drone

class Map:
    def __init__(self, path, drone_start_point):
        self.drone_start_point = drone_start_point
        try:
            img_map = Image.open(path)
            self.map = self.render_map_from_image_to_boolean(img_map)
        except IOError as e:
            print(e)


    def render_map_from_image_to_boolean(self, map_img):
        w, h = map_img.size
        map_array = [[False for _ in range(h)] for _ in range(w)]
        pixels = map_img.load()
        for y in range(h):
            for x in range(w):
                r, g, b = pixels[x, y][:3]
                if r != 0 and g != 0 and b != 0:  # think black
                    map_array[x][y] = True
        return map_array

    def is_collide(self, x, y):
        return not self.map[x][y]

    def paint(self, screen):
        gray_color = (128, 128, 128)
        for i in range(len(self.map)):
            for j in range(len(self.map[0])):
                if not self.map[i][j]:
                    screen.set_at((i, j), gray_color)

# Example usage with Pygame
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    map_image_path = 'path/to/your/map_image.png'
    drone_start_point = Point.Point(0, 0)
    game_map = Map(map_image_path, drone_start_point)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill((255, 255, 255))
        game_map.paint(screen)
        pygame.display.flip()
    
    pygame.quit()
