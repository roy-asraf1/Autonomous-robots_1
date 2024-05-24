import numpy as np

class Lidar:
    def __init__(self, range_error=0.02, max_range=3.0):
        self.range_error = range_error
        self.max_range = max_range

    def measure(self, distance):
        noise = np.random.uniform(-self.range_error, self.range_error)
        measured_distance = distance + noise
        return min(max(measured_distance, 0), self.max_range)
