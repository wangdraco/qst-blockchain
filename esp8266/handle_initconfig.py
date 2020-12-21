# -*- coding: UTF8 -*-

from machine import Pin
import machine
from time import sleep

def init_config(file, file_init):
    file_data = ""
    with open(file_init, "r", encoding="utf-8") as f:
        for line in f:
            file_data += line

    with open(file, "w", encoding="utf-8") as f:
        f.write(file_data)


def handle_init_config(pin):
    i = 0
    while True and p.value() == 0:
        print('reset begin-------------', p.value())
        sleep(1)
        i = i + 1
        if i == 3:
            print('initialing config.py files +++++++++++++')
            init_config('config.py', 'config_init.py')
            sleep(0.5)
            machine.reset()
            break


global p
p = Pin(5, Pin.IN)
p.irq(trigger=Pin.IRQ_FALLING, handler=handle_init_config)

