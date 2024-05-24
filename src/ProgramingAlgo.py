from enum import Enum
from collections import deque
import Drone
import Graph
import CPU
import Drone
import Point
import WorldParams
import Tools

class PixelState(Enum):
    BLOCKED = 1
    EXPLORED = 2
    UNEXPLORED = 3
    VISITED = 4

class ProgramingAlgo:
    def __init__(self, real_map):
        self.map_size = 3000
        self.map = [[PixelState.UNEXPLORED for _ in range(self.map_size)] for _ in range(self.map_size)]
        self.drone = Drone(real_map)
        self.drone.add_lidar(0)
        self.drone.add_lidar(90)
        self.drone.add_lidar(-90)
        self.points = []
        self.is_rotating = 0
        self.degrees_left = deque()
        self.degrees_left_func = deque()
        self.is_speed_up = False
        self.m_graph = Graph()
        self.ai_cpu = CPU(200, "Auto_AI")
        self.ai_cpu.add_function(self.update)
        self.init_map()
    
    def init_map(self):
        self.drone_starting_point = Point(self.map_size // 2, self.map_size // 2)
    
    def play(self):
        self.drone.play()
        self.ai_cpu.play()

    def update(self, delta_time):
        self.update_visited()
        self.update_map_by_lidars()
        self.ai(delta_time)

        if self.is_rotating != 0:
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
            rotation = self.drone.get_gyro_rotation() + lidar.degrees
            distance = lidar.get_simulation_distance(0)
            to_point = Tools.get_point_by_distance(from_point, rotation, distance)
            # Update map logic based on lidar data
            
    def update_visited(self):
        # Logic to update visited pixels in the map
        pass

    def ai(self, delta_time):
        # AI logic to control the drone
        pass

    def update_rotating(self, delta_time):
        if len(self.degrees_left) == 0:
            self.is_rotating = 0
            return

        degrees_left_to_rotate = self.degrees_left[0]
        is_left = degrees_left_to_rotate > 0
        degrees_left_to_rotate -= delta_time * WorldParams.rotation_per_second / 1000.0
        self.degrees_left[0] = degrees_left_to_rotate

        if (is_left and degrees_left_to_rotate <= 0) or (not is_left and degrees_left_to_rotate >= 0):
            self.degrees_left.popleft()
            func = self.degrees_left_func.popleft()
            if func:
                func()
            if len(self.degrees_left) == 0:
                self.is_rotating = 0
            return

        direction = 1 if degrees_left_to_rotate > 0 else -1
        self.drone.rotate_left(delta_time * direction)
    
    def spin_by(self, degrees, is_first=True, func=None):
        if is_first:
            self.degrees_left.appendleft(degrees)
            self.degrees_left_func.appendleft(func)
        else:
            self.degrees_left.append(degrees)
            self.degrees_left_func.append(func)
        self.is_rotating = 1
    
    def get_last_point(self):
        if len(self.points) == 0:
            return Point(0, 0)
        return self.points[-1]

    def remove_last_point(self):
        if not self.points:
            return Point(0, 0)
        return self.points.pop()
    
    def get_avg_last_point(self):
        if len(self.points) < 2:
            return Point(0, 0)
        p1 = self.points[-1]
        p2 = self.points[-2]
        return Point((p1.x + p2.x) / 2, (p1.y + p2.y) / 2)
