import math

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    
    def midpoint_to(self, other):
        return Point((self.x + other.x) / 2, (self.y + other.y) / 2)
    
    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def is_same_as(self, other):
        return self.x == other.x and self.y == other.y

    def angle_to(self, other):
        return math.degrees(math.atan2(other.y - self.y, other.x - self.x))
    
    
    def distance_to(self, other):
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)