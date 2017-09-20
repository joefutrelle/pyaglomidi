import time

def now():
    return time.time()

def in_s(s):
    return now() + s

def wait(wait_t):
    time.sleep(max(0,wait_t))

class RtQueue(object):
    def __init__(self):
        self.id = 0
        self.q = {}
    def schedule(self, callback, t, params=None):
        self.q[self.id] = (callback, t, params)
        self.id += 1
    def schedule_in(self, callback, ins, params=None):
        self.schedule(callback, in_s(ins))
    def call_next(self):
        min_k, _ = min(self.q.items(), key=lambda i: i[1][1])
        callback, t, params = self.q[min_k]
        del self.q[min_k]
        wait_t = t - now()
        wait(wait_t)
        callback(self)
    def call_all(self):
        while self.call_next() is not None:
            pass

# testing code
def test():
    import random
    def tick(queue):
        print('Tick')
        queue.schedule_in(tick, 1.0)
    def rand(queue):
        print('Random')
        queue.schedule_in(rand, random.random() * 4)
    queue = RtQueue()
    tick(queue)
    rand(queue)
    while True:
        queue.call_next()

if __name__=='__main__':
    test()