import threading
import time
from typing import List, Callable

class CPU:
    def __init__(self, hz: int, name: str):
        self.hz = hz
        self.functions_list: List[Callable[[int], None]] = []
        self.is_play = False
        self.elapsed_milli = 0
        self.is_played_before_stop = False
        self.lock = threading.Condition()
        self.thread = threading.Thread(target=self.run, name=f"Eventor_{name}")
        self.thread.start()
        self.all_cpus.append(self)

    all_cpus = []

    @staticmethod
    def stop_all_cpus():
        for cpu in CPU.all_cpus:
            cpu.stop()

    @staticmethod
    def resume_all_cpus():
        for cpu in CPU.all_cpus:
            cpu.resume()

    def resume(self):
        with self.lock:
            if self.is_played_before_stop:
                self.is_play = True
                self.lock.notify_all()

    def add_function(self, func: Callable[[int], None]):
        self.functions_list.append(func)

    def play(self):
        with self.lock:
            self.is_play = True
            self.is_played_before_stop = True
            self.lock.notify_all()

    def stop(self):
        with self.lock:
            self.is_play = False
            self.is_played_before_stop = False

    def run(self):
        while True:
            with self.lock:
                while not self.is_play:
                    self.lock.wait()
            # Implementation of function execution
