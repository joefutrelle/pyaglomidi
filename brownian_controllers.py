from itertools import chain
from time import time, sleep
from random import random, gauss, shuffle

PORT=2

import rtmidi as rt

def gen_all_off(now):
    return ((now, tuple(chain(*((0x90, n, 0) for n in range(127))))),)

def next(prev):
	prev += gauss(0,3)
	return max(0,min(prev,127))

value = [[random() * 127 for n in range(16)] for controller in range(64)]

def emitter():
    source = rt.MidiOut()
    avail_ports = source.get_ports()
    for i,p in zip(range(len(avail_ports)),avail_ports):
		print (i,p)
    if avail_ports:
        source.open_port(PORT)
    else:
        source.open_virtual_port('my virt port')
    sleep(4)

    channels = range(1)
    controllers = range(12)
    while True:
        shuffle(channels)
        shuffle(controllers)
        for channel in channels:
            for controller in controllers:
                value[controller][channel] = next(value[controller][channel])
                source.send_message((0xB0 | channel, controller, int(value[controller][channel])))
        sleep(0.15)

if __name__=='__main__':
    emitter()
