import csv
import time
from threading import Thread

class DistanceLogger:
    def __init__(self, drone, interval=0.1):
        self.drone = drone
        self.interval = interval
        self.running = False
        self.thread = None

    def calculate_distances(self):
        return {
            'forward': self.drone.x + self.drone.speed_x,
            'backward': self.drone.x - self.drone.speed_x,
            'right': self.drone.y + self.drone.speed_y,
            'left': self.drone.y - self.drone.speed_y
        }

    def _write_header(self):
        fieldnames = ['Time', 'Forward', 'Backward', 'Right', 'Left', 'Speed']
        return fieldnames

    def _get_log_data(self, start_time):
        distances = self.calculate_distances()
        speed = (self.drone.speed_x**2 + self.drone.speed_y**2)**0.5
        return {
            'Time': time.time() - start_time,
            'Forward': distances['forward'],
            'Backward': distances['backward'],
            'Right': distances['right'],
            'Left': distances['left'],
            'Speed': speed
        }

    def log_distances(self):
        with open('distance_log.csv', 'w', newline='') as csvfile:
            fieldnames = self._write_header()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            start_time = time.time()

            while self.running:
                writer.writerow(self._get_log_data(start_time))
                time.sleep(self.interval)

    def start_logging(self):
        self.running = True
        self.thread = Thread(target=self.log_distances)
        self.thread.start()

    def stop_logging(self):
        self.running = False
        if self.thread:
            self.thread.join()

    def is_logging(self):
        return self.running

    def set_interval(self, interval):
        self.interval = interval
