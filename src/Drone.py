import math

max=100
class Drone:
    def __init__(self, x, y, max_speed, acceleration, angular_speed, max_angle, flight_time):
        self.x = x
        self.y = y
        self.max_speed = max_speed
        self.acceleration = acceleration
        self.angular_speed = angular_speed
        self.max_angle = max_angle
        self.flight_time = flight_time
        self.pitch = 0
        self.roll = 0
        self.yaw = 0
        self.speed_x = 0
        self.speed_y = 0
        self.altitude = 0
        self.battery_status = flight_time

    def update_position(self):
        self.x += self.speed_x
        self.y += self.speed_y

    def update_speed(self):
        self.speed_y = self._calculate_speed(self.pitch, self.speed_y)
        self.speed_x = self._calculate_speed(self.roll, self.speed_x)

    def _calculate_speed(self, angle, speed):
        return min(self.max_speed, speed + self.acceleration * 0.1 * math.sin(math.radians(angle))) if angle != 0 else speed

    def set_orientation(self, pitch=None, roll=None, yaw=None):
        self.pitch = pitch if pitch is not None else self.pitch
        self.roll = roll if roll is not None else self.roll
        self.yaw = yaw if yaw is not None else self.yaw

    def adjust_altitude(self, change):
        self.altitude = max(0, self.altitude + change)

    def is_battery_depleted(self):
        return self.battery_status <= 0

    def reduce_battery(self, amount):
        self.battery_status = max(0, self.battery_status - amount)

    def reset_drone(self, x, y):
        self.x = x
        self.y = y
        self.pitch = self.roll = self.yaw = 0
        self.speed_x = self.speed_y = 0
        self.altitude = 0
        self.battery_status = self.flight_time