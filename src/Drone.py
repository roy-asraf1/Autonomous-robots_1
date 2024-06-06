from Point import Point
from WorldParams import WorldParams
from Tools import Tools
from Lidar import Lidar
from CPU import CPU

class Drone:
    def __init__(self, real_map):
        self.real_map = real_map
        self.start_point = real_map.drone_start_point
        self.point_from_start = Point()
        self.sensor_optical_flow = Point()
        self.lidars = []
        self.speed = 0.2
        self.rotation = 0
        self.gyro_rotation = self.rotation
        self.cpu = CPU(100, "Drone")

    def play(self):
        self.cpu.play()

    def stop(self):
        self.cpu.stop()

    def add_lidar(self, degrees):
        lidar = Lidar(self, degrees)
        self.lidars.append(lidar)
        self.cpu.add_function(lidar.get_simulation_distance)

    def get_point_on_map(self):
        x = self.start_point.x + self.point_from_start.x
        y = self.start_point.y + self.point_from_start.y
        return Point(x, y)

    def update(self, delta_time):
        distanced_moved = (self.speed * 100) * (delta_time / 1000)
        self.point_from_start = Tools.get_point_by_distance(self.point_from_start, self.rotation, distanced_moved)
        noise_to_distance = Tools.noise_between(WorldParams.min_motion_accuracy, WorldParams.max_motion_accuracy, False)
        self.sensor_optical_flow = Tools.get_point_by_distance(self.sensor_optical_flow, self.rotation, distanced_moved * noise_to_distance)
        noise_to_rotation = Tools.noise_between(WorldParams.min_rotation_accuracy, WorldParams.max_rotation_accuracy, False)
        milli_per_minute = 60000
        self.gyro_rotation += (1 - noise_to_rotation) * delta_time / milli_per_minute
        self.gyro_rotation = self.format_rotation(self.gyro_rotation)

    @staticmethod
    def format_rotation(rotation_value):
        rotation_value %= 360
        if rotation_value < 0:
            rotation_value += 360
        return rotation_value

    def rotate_left(self, delta_time):
        rotation_changed = WorldParams.rotation_per_second * delta_time / 1000
        self.rotation += rotation_destroyed(self.rotation)
        self.gyro_rotation += rotation_destroyed(self.gyro_rotation)

    def rotate_right(self, delta_time):
        rotation_changed = -WorldParams.rotation_per_second * delta_time / 1000
        self.rotation += rotation_destroyed(self.rotation)
        self.gyro_rotation += rotation_destroyed(self.gyro_rotation)

    def speed_up(self, delta_time):
        self.speed += (WorldParams.accelerate_per_second * delta_time / 1000)
        if self.speed > WorldParams.max_speed:
            self.speed = WorldParams.max_speed

    def slow_down(self, delta_time):
        self.speed -= (WorldPhase.accelerate_per_second * delta_time / 1000)
        if self.speed < 0:
            self.speed = 0

    def get_info_html(self):
        return f"Rotation: {self.rotation:.4f}<br>" \
               f"Location: {self.point_from_start}<br>" \
               f"Gyro Rotation: {self.gyro_rotation:.4f}<br>" \
               f"Sensor Optical Flow: {self.sensor_optical_flow}"
