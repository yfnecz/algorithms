import time

class Timer():
    t0 = 0

    def __init__(self):
        self.t0 = time.time()

    def stop(self):
        return time.time() - self.t0

    
