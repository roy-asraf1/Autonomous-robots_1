import Point
import Tools
import WorldParams
import Lidar
import CPU

class Drone:
    def __init__(self, realMap):
        self.realMap = realMap
        self.startPoint = realMap.drone_start_point
        self.pointFromStart = Point()
        self.sensorOpticalFlow = Point()
        self.lidars = []
        self.speed = 0.2
        self.rotation = 0
        self.gyroRotation = self.rotation
        self.cpu = CPU(100, "Drone")

    def play(self):
        self.cpu.play()

    def stop(self):
        self.cpu.stop()

    def addLidar(self, degrees):
        lidar = Lidar(self, degrees)
        self.lidars.append(lidar)
        self.cpu.addFunction(lidar.getSimulationDistance)

    def getPointOnMap(self):
        x = self.startPoint.x + self.pointFromStart.x
        y = self.startPoint.y + self.pointFromStart.y
        return Point(x, y)

    def update(self, deltaTime):
        distancedMoved = (self.speed * 100) * (deltaTime / 1000)
        self.pointFromStart = Tools.getPointByDistance(self.pointFromStart, self.rotation, distancedMoved)
        noiseToDistance = Tools.noiseBetween(WorldParams.min_motion_accuracy, WorldParams.max_motion_accuracy, False)
        self.sensorOpticalFlow = Tools.getPointByDistance(self.sensorOpticalFlow, self.rotation, distancedMoved * noiseToDistance)
        noiseToRotation = Tools.noiseBetween(WorldParams.min_rotation_accuracy, WorldParams.max_rotation_accuracy, False)
        milli_per_minute = 60000
        self.gyroRotation += (1 - noiseToRotation) * (deltaTime / milli_per_minute)
        self.gyroRotation = self.formatRotation(self.gyroRotation)

    def rotateLeft(self, deltaTime):
        rotationChanged = WorldParams.rotation_per_second * deltaTime / 1000
        self.rotation += rotationChanged
        self.rotation = self.formatRotation(self.rotation)
        self.gyroRotation += rotationChanged
        self.gyroRotation = self.formatRotation(self.gyroRotation)

    def rotateRight(self, deltaTime):
        rotationChanged = -WorldParams.rotation_per_second * deltaTime / 1000
        self.rotation += rotationChanged
        self.rotation = self.formatRotation(self.rotation)
        self.gyroRotation += rotationChanged
        self.gyroRotation = self.formatRotation(self.gyroRotation)

    def speedUp(self, deltaTime):
        self.speed += (WorldParams.accelerate_per_second * deltaTime / 1000)
        if self.speed > WorldParams.max_speed:
            self.speed = WorldParams.max_speed

    def slowDown(self, deltaTime):
        self.speed -= (WorldParams.accelerate_per_second * deltaTime / 1000)
        if self.speed < 0:
            self.speed = 0

    def formatRotation(self, rotation):
        while rotation >= 360:
            rotation -= 360
        while rotation < 0:
            rotation += 360
        return rotation

    def getOpticalSensorLocation(self):
        return Point(self.sensorOpticalFlow)
