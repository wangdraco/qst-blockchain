
import machine
from machine import UART,Pin,Timer
import time
import uasyncio as asyncio
#uart = UART(2, baudrate=115200, tx=17, rx=16, bits=8, parity=None, stop=1)
uart = UART(1, baudrate=115200, tx=25, rx=26, bits=8, parity=None, stop=1)

#通过定时器，定期的监听uart的信息
timer = Timer(1)
timer.init(period=50, mode=Timer.PERIODIC, callback=lambda t: read_uart(uart))

def read_uart(uart):
    if uart.any():
        print('received: ' + uart.read().decode('utf-8') + '\n')
        #通过定时器，定期的监听uart的信息

#read_uart(uart)

def run():
    uart.write("fsdafdsfaaafffffffffffffffffffffffffffffffffffffffffffff")


