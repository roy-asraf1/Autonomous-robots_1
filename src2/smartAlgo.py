import random
from PathMarker import PathMarker

class SmartAlgo:
    def __init__(self, map_obj, drone):
        self.map = map_obj
        self.drone = drone
        self.white_points = self.generate_random_points(1000)
        self.path_marker = PathMarker(4, (255, 255, 0))  # Radius 4 for yellow path
        self.blue_path_marker = PathMarker(2, (0, 0, 255))  # Radius 2 for blue path
        self.grey_circle_radius = 5
        self.grey_circle_color = (128, 128, 128)  # Grey color for saved points

    def generate_random_points(self, num_points):
        points = []
        while len(points) < num_points:
            x = random.randint(0, self.map.screen_width - 1)
            y = random.randint(0, self.map.screen_height - 1)
            if self.map.is_walkable(x, y):
                points.append((x, y))
        return points

    def get_next_point(self):
        if not self.white_points:
            return None
        return self.white_points.pop(0)

    def is_safe_to_move(self, x, y):
        return self.map.is_walkable(x, y) and self.check_surroundings(x, y)

    def check_surroundings(self, x, y):
        # Check all directions around the point to ensure there is enough space
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in directions:
            if not self.map.is_walkable(x + dx, y + dy):
                return False
        return True

    def move_towards_point(self, point):
        target_x, target_y = point
        if self.is_safe_to_move(target_x, target_y):
            if self.drone.x < target_x:
                self.drone.update_speed(1, 0, 0)  # Move right
            elif self.drone.x > target_x:
                self.drone.update_speed(-1, 0, 0)  # Move left
            if self.drone.y < target_y:
                self.drone.update_speed(0, 1, 0)  # Move down
            elif self.drone.y > target_y:
                self.drone.update_speed(0, -1, 0)  # Move up

            self.drone.move()
            self.path_marker.add_position((int(self.drone.x), int(self.drone.y)))
        else:
            print(f"Cannot move to ({target_x}, {target_y}) safely.")

    def run(self):
        while self.drone.check_battery() > 0 and self.white_points:
            next_point = self.get_next_point()
            if not next_point:
                break
            self.move_towards_point(next_point)
            print(f"Moving to point {next_point}, Drone position: {self.drone.get_position()}, Battery: {self.drone.check_battery()}")
            if not self.map.is_walkable(self.drone.x, self.drone.y):
                print("Hit an obstacle, moving to next point")
                self.drone.update_speed(-self.drone.speed_x, -self.drone.speed_y, 0)
                self.drone.move()
