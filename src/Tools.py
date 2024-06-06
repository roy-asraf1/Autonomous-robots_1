import math
import random
from Point import Point
from WorldParams import WorldParams

class Tools:
    @staticmethod
    def get_point_by_distance(fromPoint, rotation, distance):
        radians = math.pi * (rotation / 180)
        i = distance / WorldParams.CMPerPixel
        xi = fromPoint.x + math.cos(radians) * i
        yi = fromPoint.y + math.sin(radians) * i
        return Point(xi, yi)

    @staticmethod
    def noise_between(min, max, isNegative):
        noise = (min + random.random() * (max - min)) / 100
        if not isNegative:
            return 1 + noise
        if random.random() > 0.5:
            return 1 + noise
        else:
            return 1 - noise

    @staticmethod
    def getDistanceBetweenPoints(fromPoint, toPoint):
        x1 = (fromPoint.x - toPoint.x)**2
        y1 = (fromPoint.y - toPoint.y)**2
        return math.sqrt(x1 + y1)
