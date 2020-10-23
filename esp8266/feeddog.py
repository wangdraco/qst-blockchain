from machine import Pin
import utime,_thread

pin = Pin(27)
pin.init(mode=Pin.OUT,pull=None)  #pull = Pin.PULL_DOWN or Pin.PULL_UP


def feedfood(p4, period_ms):
    print('value +++++ ', p4.value())
    while True:
        p4.value(1)
        #print('value +++++ ',p4.value())
        utime.sleep_ms(period_ms)
        p4.value(0)
        #print('value ==== ',p4.value())
        utime.sleep_ms(period_ms)

_thread.start_new_thread(feedfood, (pin, 1000))