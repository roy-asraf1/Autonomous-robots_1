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
        # Example function to update visited pixels
        pass

    def updateMapByLidars(self):
        # Example function to update map using lidar data
        pass

    def ai(self, deltaTime):
        # Example AI function to be implemented
        pass

    def updateRotating(self, deltaTime):
        # Example function to handle rotation
        pass

    def speedUp(self):
        self.isSpeedUp = True

    def speedDown(self):
        self.isSpeedUp = False
