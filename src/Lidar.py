
import random
import WorldParams
import Tools

class Lidar:
    def __init__(self, drone, degrees):
        self.drone = drone
        self.degrees = degrees
        self.current_distance = 0

    def get_distance(self, deltaTime):
        actual_point_to_shoot = self.drone.getPointOnMap()
        rotation = self.drone.getRotation() + self.degrees
        distance_in_cm = 1
        while distance_in_cm <= WorldParams.lidar_limit:
            p = Tools.getPointByDistance(actual_point_to_shoot, rotation, distance_in_cm)
            if self.drone.realMap.is_collide(int(p.x), int(p.y)):
                break
            distance_in_cm += 1
        return distance_in_cm

    def get_simulation_distance(self, deltaTime):
        ran = random.random()
        if ran <= 0.05:  # 5% of the time, not getting an answer
            distance_in_cm = 0
        else:
            distance_in_cm = self.get_distance(deltaTime)
            distance_in_cm += random.randint(-WorldParams.lidar_noise, WorldParams.lidar_noise)
        self.current_distance = distance_in_cm
        return distance_in_cm

    def paint(self, g):
        actual_point_to_shoot = self.drone.getPointOnMap()
        from_rotation = self.drone.getRotation() + self.degrees
        to = Tools.getPointByDistance(actual_point_to_shoot, from_rotation, self.current_distance)
        g.draw_line(int(actual_point_to_shoot.x), int(actual_point_to_shoot.y), int(to.x), int(to.y))
