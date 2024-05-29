import Drone
import CPU
import Point

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

    def updateRotating(self, deltaTime):
        if len(self.degrees_left) > 0:
            degrees_left_to_rotate = self.degrees_left[0]
            direction = int(degrees_left_to_rotate / abs(degrees_left_to_rotate))
            self.drone.rotateLeft(deltaTime * direction)
            if (direction > 0 and degrees_left_to_rotate <= 0) or (direction < 0 and degrees_left_to_rotate >= 0):
                self.degrees_left.pop(0)
                func = self.degrees_left_func.pop(0)
                if func:
                    func()
                if not self.degrees_left:
                    self.isRotating = 0

    def spinBy(self, degrees, isFirst=False, func=None):
        lastGyroRotation = self.drone.getGyroRotation()
        if isFirst:
            self.degrees_left.insert(0, degrees)
            self.degrees_left_func.insert(0, func)
        else:
            self.degrees_left.append(degrees)
            self.degrees_left_func.append(func)
        self.isRotating = 1
