import uasyncio as asyncio
from machine import UART, Pin

uart = UART(2, baudrate=115200, tx=17, rx=16, bits=8, parity=None, stop=1)


# p4 = Pin(4, Pin.OUT)
# p4.value(0)

async def sender():
    swriter = asyncio.StreamWriter(uart, {})
    while True:
        # p4.value(1)
        swriter.write('Hello uart\n')
        await swriter.drain()
        # p4.value(0)

        await asyncio.sleep(2)


async def receiver():
    # p4.value(0)
    sreader = asyncio.StreamReader(uart)
    while True:
        res = await sreader.readline()
        print('Recieved', res)


async def main():
    asyncio.create_task(sender())
    asyncio.create_task(receiver())
    while True:
        await asyncio.sleep(1)


def test():
    try:

        asyncio.run(main())
    except:
        print('Interrupted')
    finally:
        asyncio.new_event_loop()
        print('as_demos.auart.test() to run again.')


test()


