
import threading
import time
from collections import deque

class CPU:
    all_cpus = []

    def __init__(self, hz, name):
        self.functions_list = deque()
        self.isPlay = False
        self.isPlayedBeforeStop = False
        self.hz = hz
        self.elapsedMilli = 0
        self.thread = threading.Thread(target=self.thread_run, name="Eventor_" + name)
        self.thread.start()
        if not CPU.all_cpus:
            CPU.all_cpus = []
        CPU.all_cpus.append(self)

    @staticmethod
    def stopAllCPUS():
        for cpu in CPU.all_cpus:
            cpu.isPlay = False

    @staticmethod
    def resumeAllCPUS():
        for cpu in CPU.all_cpus:
            cpu.resume()

    def resume(self):
        if self.isPlayedBeforeStop:
            self.isPlay = True
            with self.thread:
                self.thread.notify()

    def addFunction(self, func):
        self.functions_list.append(func)

    def play(self):
        self.isPlay = True
        self.isPlayedBeforeStop = True
        self.resume()

    def stop(self):
        self.isPlay = False
        self.isPlayedBeforeStop = False

    def getElapsedMilli(self):
        return self.elapsedMilli

    def resetClock(self):
        self.elapsedMilli = 0

    def thread_run(self):
        time.sleep(0.01)  # Sleep for 10 ms (0.01 seconds)
        
        functions_size = 0
        last_sample_times = None
        i = 0
        while True:
            if functions_size != len(self.functions_list):
                functions_size = len(self.functions_list)
                last_sample_times = [0] * functions_size
            if functions_size == 0:
                continue
            last_sample = time.time()
            time.sleep(max(0, 1 / self.hz))
            with threading.Lock():
                while not self.isPlay:
                    threading.Condition().wait()
                    last_sample = time.time()
            diff = int((time.time() - last_sample) * 1000)
            before_index = (i - 1) % functions_size
            actual_diff = last_sample_times[before_index] + diff - last_sample_times[i]
            last_sample_times[i] = last_sample_times[before_index] + diff
            curr_func = self.functions_list[i]
            curr_func(actual_diff)
            self.elapsedMilli += actual_diff
            i = (i + 1) % functions_size
