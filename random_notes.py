from itertools import chain
from heapq import heappush, heappop
from time import time, sleep
from random import random, randint, gauss
import math

import rtmidi as rt

PORT=2
LOOP_WAIT = 1.0 / 200  # 200 Hz

def gen_all_off(now):
    return ((now, tuple(chain(*((0x90, n, 0) for n in range(127))))),)

def gen_random_notes(now):
    pitch = randint(0, 96)
    velocity = randint(80, 127)
    duration = math.fabs(gauss(0,0.75))
    return ((now, (0x90, pitch, velocity)),
            (now + duration, (0x80, pitch, 0)))

def maybe_gen_notes(now):
    probability = 0.01
    if random() < probability:
        return gen_random_notes(now)
    else:
        return ()

def heappush_all(heap, seq):
    for item in seq:
        heappush(heap, item)


def emitter():
    source = rt.MidiOut()
    avail_ports = source.get_ports()
    print avail_ports
    if avail_ports:
        source.open_port(PORT)
    else:
        source.open_virtual_port('my virt port')

    sleep(4)

    frames = []

    frame_time = time()
    heappush_all(frames, gen_all_off(frame_time))
    while True:
        heappush_all(frames, maybe_gen_notes(frame_time))
        while frames and (frames[0][0] < frame_time):
            midi_out = heappop(frames)
            print "emit {}".format(midi_out[1])
            source.send_message(midi_out[1])

        now = time()
        wait_time = -1
        while wait_time <= 0:
            frame_time = frame_time + LOOP_WAIT
            wait_time = frame_time - now
        sleep(wait_time)

if __name__=='__main__':
    emitter()
