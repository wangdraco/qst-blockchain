



import machine
from machine import UART,Pin,Timer
uart = UART(2, baudrate=115200, tx=17, rx=16, bits=8, parity=None, stop=1)

def _handleOnReceive(pin):
    print(uart.read())
    if(uart.read()):
      print(uart.readline())
#p6 = Pin(16,Pin.IN)
#p6.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING,handler=_handleOnReceive)


#通过定时器，定期的监听uart的信息
timer = Timer(1)
timer.init(period=50, mode=Timer.PERIODIC, callback=lambda t: read_uart(uart))

def read_uart(uart):
    if uart.any():
        print('received: ' + uart.read().decode('utf-8') + '\n')


