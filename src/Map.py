from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import Point

class Map:
    def __init__(self, path, drone_start_point):
        self.drone_start_point = drone_start_point
        try:
            img_map = Image.open(path).convert('RGB')
            self.map = self.render_map_from_image_to_boolean(img_map)
        except IOError as e:
            print(e)

    def render_map_from_image_to_boolean(self, map_img):
        w, h = map_img.size
        map_array = np.array(map_img)
        map_bool = np.zeros((w, h), dtype=bool)
        for y in range(h):
            for x in range(w):
                r, g, b = map_array[y, x]
                if r != 0 and g != 0 and b != 0:  # think black
                    map_bool[x, y] = True
        return map_bool

    def is_collide(self, x, y):
        return not self.map[x, y]

    def paint(self):
        plt.imshow(self.map, cmap='gray')
        plt.show()

# Usage example:
if __name__ == "__main__":
    start_point = Point(0, 0)  # Assuming Point class is defined somewhere
    map_instance = Map('path_to_image.png', start_point)
    map_instance.paint()
