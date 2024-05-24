import math

class Painter:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.color = (0, 0, 0)  # Black in RGB
        self.direction = 0

    def move(self, distance):
        self.x += distance * math.cos(self.direction)
        self.y += distance * math.sin(self.direction)

    def turn(self, angle):
        self.direction += angle

    def set_color(self, new_color):
        if isinstance(new_color, tuple) and len(new_color) == 3:
            self.color = new_color
        else:
            raise ValueError("Color must be an RGB tuple")

    def set_color_rgb(self, red, green, blue):
        self.color = (red, green, blue)

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_color(self):
        return self.color
