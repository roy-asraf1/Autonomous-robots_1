from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import Point
import Lidar
import CPU
import Tools
import WorldParams

class Drone:
    def __init__(self, real_map):
        self.gyro_rotation = 0.0
        self.sensor_optical_flow = Point(0, 0)
        self.point_from_start = Point(0, 0)
        self.start_point = real_map.drone_start_point
        self.lidars = []
        self.drone_img_path = "D:/Tests/drone_3_pixels.png"
        self.real_map = real_map
        self.rotation = 0.0
        self.speed = 0.2
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
        distanced_moved = (self.speed * 100) * (delta_time / 1000.0)
        self.point_from_start = Tools.get_point_by_distance(self.point_from_start, self.rotation, distanced_moved)
        
        noise_to_distance = Tools.noise_between(WorldParams.min_motion_accuracy, WorldParams.max_motion_accuracy, False)
        self.sensor_optical_flow = Tools.get_point_by_distance(self.sensor_optical_flow, self.rotation, distanced_moved * noise_to_distance)
        
        noise_to_rotation = Tools.noise_between(WorldParams.min_rotation_accuracy, WorldParams.max_rotation_accuracy, False)
        milli_per_minute = 60000
        self.gyro_rotation += (1 - noise_to_rotation) * delta_time / milli_per_minute
        self.gyro_rotation = self.format_rotation(self.gyro_rotation)

    def format_rotation(self, rotation):
        while rotation < 0:
            rotation += 360
        while rotation >= 360:
            rotation -= 360
        return rotation

    def get_optical_sensor_location(self):
        return Point(self.sensor_optical_flow)

    def rotate_left(self, delta_time):
        rotation_changed = WorldParams.rotation_per_second * delta_time / 1000.0
        self.rotation += rotation_changed
        self.rotation = self.format_rotation(self.rotation)
        
        self.gyro_rotation += rotation_changed
        self.gyro_rotation = self.format_rotation(self.gyro_rotation)

    def rotate_right(self, delta_time):
        rotation_changed = -WorldParams.rotation_per_second * delta_time / 1000.0
        self.rotation += rotation_changed
        self.rotation = self.format_rotation(self.rotation)
        
        self.gyro_rotation += rotation_changed
        self.gyro_rotation = self.format_rotation(self.gyro_rotation)

    def speed_up(self, delta_time):
        self.speed += WorldParams.accelerate_per_second * delta_time / 1000.0
        if self.speed > WorldParams.max_speed:
            self.speed = WorldParams.max_speed

    def slow_down(self, delta_time):
        self.speed -= WorldParams.accelerate_per_second * delta_time / 1000.0
        if self.speed < 0:
            self.speed = 0

    def paint(self):
        if not hasattr(self, 'm_image'):
            try:
                self.m_image = Image.open(self.drone_img_path)
            except Exception as ex:
                print(ex)
        
        plt.imshow(self.m_image)
        plt.show()
        
        for lidar in self.lidars:
            lidar.paint()

    def get_info_html(self):
        info = "<html>"
        info += f"Rotation: {self.rotation:.4f}<br>"
        info += f"Location: {self.point_from_start}<br>"
        info += f"gyroRotation: {self.gyro_rotation:.4f}<br>"
        info += f"sensorOpticalFlow: {self.sensor_optical_flow}<br>"
        info += "</html>"
        return info
