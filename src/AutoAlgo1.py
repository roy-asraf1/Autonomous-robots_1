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
        self.toggle_ai = False
        self.toggle_center_ai = False
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
        self.drone_path = []  # List to store the drone's path
        self.lidar_lines = []  # List to store the lidar lines
        self.is_init = True
        self.last_front_lidar_dis = 0
        self.is_rotate_right = False
        self.changed_right = 0
        self.changed_left = 0
        self.try_to_escape = False
        self.left_or_right = 1
        self.max_rotation_to_direction = 20
        self.is_finish = True
        self.is_left_right_rotation_enable = True
        self.is_risky = False
        self.max_risky_distance = 150
        self.try_to_escape = False
        self.risky_dis = 0
        self.max_angle_risky = 10
        self.is_lidars_max = False
        self.save_point_after_seconds = 3
        self.max_distance_between_points = 100
        self.init_point = None

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
        if self.toggle_ai:
            self.ai()
        if self.toggle_center_ai:
            self.center_ai()
        self.drone.update(delta_time)  # Update the drone's position
        self.drone_path.append(self.drone.get_point_on_map())  # Store the current position
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
            lidar_line = []  # Store the lidar line points
            for distance_in_cm in range(lidar.current_distance):
                p = Tools.get_point_by_distance(from_point, rotation, distance_in_cm)
                self.set_pixel(p.x, p.y, PixelState.EXPLORED)
                lidar_line.append((p.x, p.y))  # Add the point to the lidar line
            if lidar.current_distance > 0 and lidar.current_distance < WorldParams.lidar_limit - WorldParams.lidar_noise:
                p = Tools.get_point_by_distance(from_point, rotation, lidar.current_distance)
                self.set_pixel(p.x, p.y, PixelState.BLOCKED)
                lidar_line.append((p.x, p.y))  # Add the final point to the lidar line
            self.lidar_lines.append(lidar_line)  # Store the lidar line

    def update_visited(self):
        drone_point = self.drone.get_optical_sensor_location()
        from_point = Point(drone_point.x + self.drone_starting_point.x, drone_point.y + self.drone_starting_point.y)
        self.set_pixel(from_point.x, from_point.y, PixelState.VISITED)

    def set_pixel(self, x, y, state):
        xi, yi = int(x), int(y)
        if 0 <= xi < self.map_size and 0 <= yi < self.map_size:
            if state == PixelState.VISITED or self.map[xi][yi] == PixelState.UNEXPLORED:
                self.map[xi][yi] = state

    def ai(self):
        if self.is_init:
            self.speed_up()
            drone_point = self.drone.get_optical_sensor_location()
            self.init_point = Point(drone_point.x, drone_point.y)
            self.points.append(drone_point)
            # self.mGraph.add_vertex(drone_point)  # Assuming mGraph is defined somewhere
            self.is_init = False

        drone_point = self.drone.get_optical_sensor_location()

        if not self.is_risky:
            lidar = self.drone.lidars[0]
            if lidar.current_distance <= self.max_risky_distance:
                self.is_risky = True
                self.risky_dis = lidar.current_distance

            lidar1 = self.drone.lidars[1]
            if lidar1.current_distance <= self.max_risky_distance / 3:
                self.is_risky = True

            lidar2 = self.drone.lidars[2]
            if lidar2.current_distance <= self.max_risky_distance / 3:
                self.is_risky = True
        else:
            if not self.try_to_escape:
                self.try_to_escape = True
                lidar1 = self.drone.lidars[1]
                a = lidar1.current_distance

                lidar2 = self.drone.lidars[2]
                b = lidar2.current_distance

                spin_by = self.max_angle_risky

                if a > 270 and b > 270:
                    self.is_lidars_max = True
                    l1 = Tools.get_point_by_distance(drone_point, lidar1.degrees + self.drone.gyro_rotation,
                                                     lidar1.current_distance)
                    l2 = Tools.get_point_by_distance(drone_point, lidar2.degrees + self.drone.gyro_rotation,
                                                     lidar2.current_distance)
                    last_point = self.get_avg_last_point()
                    dis_to_lidar1 = Tools.get_distance_between_points(last_point, l1)
                    dis_to_lidar2 = Tools.get_distance_between_points(last_point, l2)
                    spin_by = 90

                    if dis_to_lidar1 < dis_to_lidar2:
                        spin_by *= -1
                else:
                    if a < b:
                        spin_by *= -1

                self.spin_by(spin_by, True, self.escape_risk)

    def center_ai(self):
        # Center AI logic
        if not self.is_risky:
            lidar_left = self.drone.lidars[1]
            lidar_right = self.drone.lidars[2]

            if lidar_left.current_distance < self.max_risky_distance / 2 or lidar_right.current_distance < self.max_risky_distance / 2:
                self.is_risky = True

                if lidar_left.current_distance < lidar_right.current_distance:
                    self.spin_by(-self.max_angle_risky, True, self.escape_risk)  # Spin right
                else:
                    self.spin_by(self.max_angle_risky, True, self.escape_risk)  # Spin left

        else:
            self.try_to_escape = True

    def escape_risk(self):
        self.try_to_escape = False
        self.is_risky = False

    def update_rotating(self, delta_time):
        if not self.degrees_left:
            return  # No rotation needed

        current_degrees = self.degrees_left.pop(0)
        func = self.degrees_left_func.pop(0) if self.degrees_left_func else None
        self.drone.rotate_left(current_degrees)  # Assuming rotate_left method exists in Drone class

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

    def get_last_point(self):
        if not self.points:
            return self.init_point
        return self.points[-1]

    def remove_last_point(self):
        if not self.points:
            return self.init_point
        return self.points.pop()

    def get_avg_last_point(self):
        if len(self.points) < 2:
            return self.init_point
        p1 = self.points[-1]
        p2 = self.points[-2]
        return Point((p1.x + p2.x) / 2, (p1.y + p2.y) / 2)

    def paint(self, surface):
        # Draw the drone's path
        for point in self.drone_path:
            pygame.draw.circle(surface, (0, 0, 255), (int(point.x), int(point.y)), 2)

        # Draw the lidar lines
        for lidar_line in self.lidar_lines:
            if len(lidar_line) > 1:
                pygame.draw.lines(surface, (255, 255, 0), False, [(int(x), int(y)) for x, y in lidar_line], 1)

        # Draw the drone
        self.drone.paint(surface)
