
import Point
import CPU
import Drone
from enum import Enum

class PixelState(Enum):
    blocked = 0
    explored = 1
    unexplored = 2
    visited = 3

class AutoAlgo1:
    def __init__(self, realMap):
        self.map_size = 3000
        self.map = [[PixelState.unexplored for _ in range(self.map_size)] for _ in range(self.map_size)]
        self.drone = Drone(realMap)
        self.drone.addLidar(0)
        self.drone.addLidar(90)
        self.drone.addLidar(-90)
        self.initMap()
        self.isRotating = 0
        self.degrees_left = []
        self.degrees_left_func = []
        self.points = []
        self.ai_cpu = CPU(200, "Auto_AI")
        self.ai_cpu.addFunction(self.update)
        self.isSpeedUp = False

    def initMap(self):
        self.droneStartingPoint = Point(self.map_size / 2, self.map_size / 2)

    def play(self):
        self.drone.play()
        self.ai_cpu.play()

    def update(self, deltaTime):
        self.updateVisited()
        self.updateMapByLidars()
        self.ai(deltaTime)
        if self.isRotating != 0:
            self.updateRotating(deltaTime)
        if self.isSpeedUp:
            self.drone.speedUp(deltaTime)
        else:
            self.drone.slowDown(deltaTime)

    def updateVisited(self):
        pass

    def updateMapByLidars(self):
        dronePoint = self.drone.getOpticalSensorLocation()
        fromPoint = Point(dronePoint.x + self.droneStartingPoint.x, dronePoint.y + self.droneStartingPoint.y)
        for lidar in self.drone.lidars:
            rotation = self.drone.getGyroRotation() + lidar.degrees
            lidar.updateMap(self.map, fromPoint, rotation)

    def ai(self, deltaTime):
        pass
    def play(self):
        self.drone.play()
        self.ai_cpu.play()

    def update(self, delta_time):
        self.update_visited()
        self.update_map_by_lidars()
        self.ai(delta_recycle, delta_time)
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
                p = self.get_point_by_distance(from_point, rotation, distance_in_cm)
                self.set_pixel(p.x, p.y, PixelState.explored)
            if lidar.current_distance > 0:
                p = self.get_point_by_distance(from_point, rotation, lidar.current_distance)
                self.set_pixel(p.x, p.y, PixelState.blocked)

    def update_visited(self):
        drone_point = self.drone.get_optical_sensor_location()
        from_point = Point(drone_point.x + self.drone_starting_point.x, drone_point.y + self.drone_starting_point.y)
        self.set_pixel(from_point.x, from_point.y, PixelState.visited)

    def set_pixel(self, x, y, state):
        xi = int(x)
        yi = int(y)
        if state == PixelState.visited or self.map[xi][yi] == PixelState.unexplored:
            self.map[xi][yi] = state


    def spinBy(self, degrees, isFirst=False, func=None):
        if isFirst:
            self.degrees_left.insert(0, degrees)
            self.degrees_left_func.insert(0, func)
        else:
            self.degrees_left.append(degrees)
            self.degrees_left_func.append(func)
        self.isRotating = 1
