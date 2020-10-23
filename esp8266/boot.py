# -*- coding: UTF8 -*-
# This file is executed on every boot (including wake-boot from deepsleep)
# Author: Draco.Wang <1599980410@qq.com>
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()


from machine import Pin
pin = Pin(27)
pin.init(mode=Pin.OUT,pull=None)

import utime,_thread
def feedfood(p, period_ms):
    while True:
        p.value(1)
        #print('value +++++ ',p4.value())
        utime.sleep_ms(period_ms)
        p.value(0)
        #print('value ==== ',p4.value())
        utime.sleep_ms(period_ms)

_thread.start_new_thread(feedfood, (pin, 1000))