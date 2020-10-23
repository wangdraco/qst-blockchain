from machine import Pin
from time import sleep_ms

def blink(gpio=2, times=1, on_ms=100, off_ms=20):
    pin_led = Pin(gpio, Pin.OUT)
    """short blink LED on GPIO pin"""
    for i in range(times):
        pin_led.value(0)
        sleep_ms(on_ms)
        pin_led.value(1)
        sleep_ms(off_ms)

