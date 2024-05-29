
import math
import random
import WorldParams
import Point

class Tools:
    @staticmethod
    def get_point_by_distance(from_point, rotation, distance):
        radians = math.pi * (rotation / 180)
        i = distance / WorldParams.CM_PER_PIXEL
        xi = from_point.x + math.cos(radians) * i
        yi = from_point.y + math.sin(radians) * i
        return Point(xi, yi)

    @staticmethod
    def noise_between(min, max, is_negative):
        noise_to_distance = 1
        noise = (min + random.random() * (max - min)) / 100
        if not is_negative:
            return noise_to_distance + noise
        if random.choice([True, False]):
            return noise_to_distance + noise
        else:
            return noise_to_distance - noise

    @staticmethod
    def get_rotation_between_points(from_point, to_point):
        y1 = from_point.y - to_point.y
        x1 = from_point.x - to_point.x
        radians = math.atan2(y1, x1)
        rotation = radians * 180 / math.pi
        return rotation

    @staticmethod
    def get_distance_between_points(from_point, to_point):
        x1 = (from_point.x - to_point.x) ** 2
        y1 = (from_point.y - to_point.y) ** 2
        return math.sqrt(x1 + y1)
