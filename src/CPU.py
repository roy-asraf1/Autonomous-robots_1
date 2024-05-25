import time
from smartDrone import SmartDrone
from Lidar import Lidar
from smartAlgo import SmartAlgo
import numpy as np


class CPU:
    def __init__(self, map_obj):
        self.drone = SmartDrone(start_x=50, start_y=50)  # Starting position
        self.lidar = Lidar()
        self.map = map_obj
        self.sensor_data = []
        self.algo = SmartAlgo(map_obj, self.drone)

    def gather_sensor_data(self):
        # Simulate gathering data from sensors
        distances = [self.lidar.measure(dist) for dist in self.get_distances()]
        yaw = self.drone.yaw
        speed_x = self.drone.speed_x
        speed_y = self.drone.speed_y
        z = self.drone.z
        baro = self.drone.z
        bat = self.drone.check_battery()
        pitch = self.drone.pitch
        roll = self.drone.roll
        accX = self.drone.speed_x
        accY = self.drone.speed_y
        accZ = self.drone.speed_z
        self.sensor_data = [distances, yaw, speed_x, speed_y, z, baro, bat, pitch, roll, accX, accY, accZ]

    def get_distances(self):
        # Simulate distances from lidar in six directions
        directions = [
            (self.drone.x, self.drone.y - 1),  # forward
            (self.drone.x, self.drone.y + 1),  # backward
            (self.drone.x + 1, self.drone.y),  # right
            (self.drone.x - 1, self.drone.y),  # left
            (self.drone.x, self.drone.y)  # up/down (2D, so just return current position)
        ]
        distances = []
        for direction in directions:
            distance = self.calculate_distance(direction)
            distances.append(distance)
        return distances

    def calculate_distance(self, direction):
        x, y = direction
        if 0 <= x < self.map.screen_width and 0 <= y < self.map.screen_height:
            if self.map.is_walkable(x, y):
                return np.linalg.norm([self.drone.x - x, self.drone.y - y])
            else:
                return self.lidar.max_range
        return self.lidar.max_range

    def run(self):
        self.gather_sensor_data()
        self.algo.run()
        print(f"Drone position: {self.drone.get_position()}, Battery: {self.drone.check_battery()}")

# Example usage
if __name__ == "__main__":
    from Map import Map
    map_obj = Map("Maps/p12.png", 1000, 800)  # Load the map
    cpu = CPU(map_obj)
    cpu.run()

