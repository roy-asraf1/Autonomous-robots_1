from CPU import CPU
from Drone import Drone
from enum import Enum
from WorldParams import WorldParams
from Tools import Tools
from Point import Point

class AutoAlgo1:
    class PixelState(Enum):
        BLOCKED = 1
        EXPLORED = 2
        UNEXPLORED = 3
        VISITED = 4

    def __init__(self, real_map):
        self.map_size = 3000
        self.map = [[self.PixelState.UNEXPLORED for _ in range(self.map_size)] for _ in range(self.map_size)]
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

    def init_map(self):
        self.drone_starting_point = Point(self.map_size / 2, self.map_size / 2)
        for i in range(self.map_size):
            for j in range(self.map_size):
                self.map[i][j] = self.PixelState.UNEXPLORED

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

    def update_map_by_lidars(self):
        drone_point = self.drone.get_optical_sensor_location()
        from_point = Point(drone_point.x + self.drone_starting_point.x, drone_point.y + self.drone_starting_point.y)
        for lidar in self.drone.lidars:
            rotation = self.drone.get_gyro_rotation() + lidar.degrees
            for distance_in_cm in range(lidar.current_distance):
                p = Tools.get_point_by_distance(from_point, rotation, distance_in_cm)
                self.set_pixel(p.x, p.y, self.PixelState.EXPLORED)
            if lidar.current_distance > 0 and lidar.current_distance < WorldParams.lidar_limit - WorldParams.lidar_noise:
                p = Tools.get_point_by_distance(from_point, rotation, lidar.current_distance)
                self.set_pixel(p.x, p.y, self.PixelIState.BLOCKED)

    def update_visited(self):
        drone_point = self.drone.get_optical_sensor_location()
        from_point = Point(drone_point.x + self.drone_starting_point.x, drone_point.y + self.drone_starting_point.y)
        self.set_pixel(from_point.x, from_point.y, self.PixelState.VISITED)

    def set_pixel(self, x, y, state):
        xi, yi = int(x), int(y)
        if self.map[xi][yi] == self.PixelState.UNEXPLORED:
            self.map[xi][yi] = state
        elif state == self.PixelState.VISITED:
            self.map[xi][yi] = state

    def ai(self, delta_time):
        # AI logic here, omitted for brevity
        pass

    def update_rotating(self, delta_time):
        # Rotating logic here, omitted for brevity
        pass

    def spin_by(self, degrees, is_first, func=None):
        # Spin handling logic here, omitted for brevity
        pass

    def paint(self, surface):
        # Implement painting logic
        # For now, just pass or add a simple drawing
        pass
