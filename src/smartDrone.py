import numpy as np
from Drone import Drone

class SmartDrone(Drone):
    def __init__(self, start_x, start_y, start_battery=480, max_speed=3.0):
        super().__init__(start_x, start_y, max_speed, 0.2, 100, 10, start_battery)
        self.home_x = start_x
        self.home_y = start_y

    def return_to_home(self):
        self.speed_x = (self.home_x - self.x) / max(abs(self.home_x - self.x), 1)
        self.speed_y = (self.home_y - self.y) / max(abs(self.home_y - self.y), 1)

    def check_battery(self):
        return self.battery_status

    def get_home_position(self):
        return self.home_x, self.home_y
