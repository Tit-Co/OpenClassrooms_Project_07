import time


class Timer:
    def __init__(self):
        self.start = time.perf_counter()

    def restart(self):
        self.start = time.perf_counter()

    def get_time(self):
        return time.perf_counter() - self.start