import pygame
from CPU import CPU
from Drone import Drone
from enum import Enum
from WorldParams import WorldParams
from Tools import Tools
from Point import Point

class PixelState(Enum):
    BLOCKED = 1
    EXPLORED = 2
    UNEXPLORED = 3
    VISITED = 4

class AutoAlgo1:
    def __init__(self, real_map):
        self.map_size = 3000
        self.map = [[PixelState.UNEXPLORED for _ in range(self.map_size)] for _ in range(self.map_size)]
        self.drone = Drone(real_map)
        self.drone.add_lidar(0)
        self.drone.add_lidar(90)
        self.drone.add_lidar(-90)
        self.init_map()
        self.ai_cpu = CPU(200, "Auto_AI")
        self.ai_cpu.add_function(self.update)
        self.points = []
        self.degrees_left = []
        self.degrees_left_func = []
        self.is_rotating = False
        self.is_speed_up = False

    def init_map(self):
        self.drone_starting_point = Point(self.map_size / 2, self.map_size / 2)
        for i in range(self.map_size):
            for j in range(self.map_size):
                self.map[i][j] = PixelState.UNEXPLORED

    def play(self):
        self.drone.play()
        self.ai_cpu.play()

    def update(self, delta_time):
        self.update_visited()
        self.update_map_by_lidars()
        self.ai(delta_time)
        self.drone.update(delta_time)  # Update the drone's position
        if self.is_rotating:
            self.update_rotating(delta_time)
        if self.is_speed_up:
            self.drone.speed_up(delta_time)
        else:
            self.drone.slow_down(delta_time)

    def speed_up(self):
        self.is_speed_up = True

    def speed_down(self):
        self.is_speed_up = False

    def update_map_by_lidars(self):
        drone_point = self.drone.get_optical_sensor_location()
        from_point = Point(drone_point.x + self.drone_starting_point.x, drone_point.y + self.drone_starting_point.y)
        for lidar in self.drone.lidars:
            rotation = self.drone.gyro_rotation + lidar.degrees
            for distance_in_cm in range(lidar.current_distance):
                p = Tools.get_point_by_distance(from_point, rotation, distance_in_cm)
                self.set_pixel(p.x, p.y, PixelState.EXPLORED)
            if lidar.current_distance > 0 and lidar.current_distance < WorldParams.lidar_limit - WorldParams.lidar_noise:
                p = Tools.get_point_by_distance(from_point, rotation, lidar.current_distance)
                self.set_pixel(p.x, p.y, PixelState.BLOCKED)

    def update_visited(self):
        drone_point = self.drone.get_optical_sensor_location()
        from_point = Point(drone_point.x + self.drone_starting_point.x, drone_point.y + self.drone_starting_point.y)
        self.set_pixel(from_point.x, from_point.y, PixelState.VISITED)

    def set_pixel(self, x, y, state):
        xi, yi = int(x), int(y)
        if 0 <= xi < self.map_size and 0 <= yi < self.map_size:
            self.map[xi][yi] = state

    def ai(self, delta_time):
        # AI logic, implement based on specific requirements
        pass

    def update_rotating(self, delta_time):
        if not self.degrees_left:
            return  # No rotation needed
        current_degrees = self.degrees_left.pop(0)
        func = self.degrees_left_func.pop(0) if self.degrees_left_func else None
        self.drone.rotate_left(current_degrees)  # Ensure rotate_left method exists in Drone class
        if func:
            func()

    def spin_by(self, degrees, is_first=False, func=None):
        if is_first:
            self.degrees_left.insert(0, degrees)
            self.degrees_left_func.insert(0, func)
        else:
            self.degrees_left.append(degrees)
            self.degrees_left_func.append(func)
        self.is_rotating = True

    def paint(self, surface):
        # Draw the drone at its current position on the surface
        drone_pos = self.drone.get_point_on_map()  # Ensure this method returns the correct position
        pygame.draw.circle(surface, (255, 0, 0), [int(drone_pos.x), int(drone_pos.y)], 5)  # Draw drone as a red circle
        self.drone.paint(surface)  # Draw the drone's lidars
