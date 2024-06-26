import random

import pygame

from WorldParams import WorldParams
from Tools import Tools
import Drone
from Point import Point


class Lidar:
    def __init__(self, drone: 'Drone', degrees: float):
        self.drone = drone
        self.degrees = degrees
        self.current_distance = 0
        self.local_counter = 0

    def get_distance(self, delta_time):
        actual_point_to_shoot = self.drone.get_point_on_map()
        rotation = self.drone.rotation + self.degrees
        distance_in_cm = 1
        while distance_in_cm <= WorldParams.lidar_limit:
            point = Tools.get_point_by_distance(actual_point_to_shoot, rotation, distance_in_cm)
            if self.drone.real_map.is_collide(int(point.x), int(point.y)):
                break
            distance_in_cm += 1
        return distance_in_cm

    def get_simulation_distance(self, delta_time):
        if random.random() <= 0.05:
            distance_in_cm = 0
        else:
            distance_in_cm = self.get_distance(delta_time)
            distance_in_cm += random.randint(-WorldParams.lidar_noise, WorldParams.lidar_noise)
        self.current_distance = distance_in_cm
        return distance_in_cm

    def paint(self, surface, drone_rotation):
        self.local_counter += 1
        start_point = self.drone.get_point_on_map()
        end_angle = drone_rotation + self.degrees
        end_point = Tools.get_point_by_distance(start_point, end_angle, self.current_distance)
        pygame.draw.line(surface, (0, 255, 0), (int(start_point.x), int(start_point.y)), (int(end_point.x), int(end_point.y)))