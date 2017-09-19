import random

class Brown(object):
    def __init__(self, min=0, max=127, step=1):
        self.value = min + ((max - min) // 2)
        self.min = min
        self.max = max
        self.step = step
    def next(self):
        self.value += random.randint(0 - self.step, self.step)
        self.value = max(self.min, self.value)
        self.value = min(self.max, self.value)
        return self.value