import CPU
import Drone
import Point

class AutoAlgo1:
    def __init__(self, realMap):
        self.map_size = 3000
        self.map = [[PixelState.UNEXPLORED for _ in range(self.map_size)] for _ in range(self.map_size)]
        self.drone = Drone(realMap)
        self.drone.addLidar(0)
        self.drone.addLidar(90)
        self.drone.addLidar(-90)
        self.initMap()
        self.degrees_left = []
        self.degrees_left_func = []
        self.points = []
        self.isRotating = 0
        self.ai_cpu = CPU(200, "Auto_AI")
        self.ai_cpu.addFunction(self.update)
        self.isSpeedUp = False

    def initMap(self):
        self.droneStartingPoint = Point(self.map_size // 2, self.map_size // 2)

    def play(self):
        self.drone.play()
        self.ai_cpu.play()

    def update(self, deltaTime):
        self.updateVisited()
        self.updateMapByLidars(deltaTime)
        self.ai(deltaTime)
        if self.isRotating:
            self.updateRotating(deltaTime)
        if self.isSpeedUp:
            self.drone.speedUp(deltaTime)
        else:
            self.drone.slowDown(deltaTime)

    def updateVisited(self):
        # Update the visited cells in the map based on drone's current position
        pass

    def updateMapByLidars(self, deltaTime):
        # Assuming map updating logic based on Lidar data goes here
        pass

    def ai(self, deltaTime):
        # AI logic to control the drone's behavior based on sensor data
        pass

    def updateRotating(self, deltaTime):
        if self.degrees_left:
            rotate_amount = self.degrees_left.pop(0)
            self.drone.rotate(rotate_amount)

    def spinBy(self, degrees, isFirst=False, func=None):
        if isFirst:
            self.degrees_left.insert(0, degrees)
        else:
            self.degrees_left.append(degrees)
        if func:
            self.degrees_left_func.append(func)
        self.isRotating = 1

    def stop(self):
        self.drone.stop()
        self.ai_cpu.stop()

