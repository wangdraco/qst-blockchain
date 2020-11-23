import uasyncio as asyncio
import socket as socket

def beat_heart():

    sock = socket.socket()
    sock.connect(('139.129.200.70', 9997))
    sock.send(("test-----").encode('utf-8'))  # data+'\n'
    print('send beat ',"test---")
    sock.close()

class Multitask():
    def __init__(self,_sleep = 10):
        self.sleep = _sleep

    async def gc_collect(self):
        import gc
        while True:
            try:
                gc.collect()
            except Exception as e:
                print('gc error',e)
            await asyncio.sleep(self.sleep)  # Pause 4s

    async def beat(self):
        while True:
            #sock = socket.socket()
            try:
                beat_heart()
            except Exception as e:
                print('beat heart socket error', e)
            await asyncio.sleep(self.sleep)  # Pause 4s


async def main_task(duration):

    if True:
        _gc = Multitask(600) #10分钟gc.collect()
        asyncio.create_task(_gc.gc_collect())
    if True:
        beat_task = Multitask(3)
        asyncio.create_task(beat_task.beat())

    while True:
        await asyncio.sleep(1)

def run(duration=10):
    try:
        asyncio.run(main_task(duration))
    except Exception as e:
        print('Interrupted',e)
    finally:
        asyncio.new_event_loop()
        print('asyncio run again.')

run()
