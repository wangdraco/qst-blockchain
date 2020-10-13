import uasyncio


#设置Pin4的状态，控制reset
#在boot.py中，先初始化pin27为无上拉和下拉模式
'''
from machine import Pin
pin = Pin(27)
pin.init(mode=Pin.OUT,pull=None)
print('value = ',pin.value())
'''
async def food(p4, period_ms):
    while True:
        p4.value(1)
        print('value +++++ ',p4.value())
        await uasyncio.sleep_ms(period_ms)
        p4.value(0)
        print('value ==== ',p4.value())
        await uasyncio.sleep_ms(period_ms)

async def main(pin):
    loop = uasyncio.get_event_loop()
    loop.create_task(food(pin, 1000))
    loop.run_forever()
    #await uasyncio.sleep_ms(5)

def feed_dog():
    from machine import Pin
    pin = Pin(4,Pin.OUT)
    uasyncio.run(main(pin))

feed_dog()

