import config as conf
import uasyncio as asyncio

if conf.sta_mode:
    from my_app import WiFi
    wifi = WiFi()
    wifi.connect()

# if conf.ap_mode:
#     from my_app import WiFi
#     wifi = WiFi()
#     wifi.ap()

async def main_task(duration):
    from my_app import Multitask

    if conf.gc_collect:
        _gc = Multitask(600) #10分钟gc.collect()
        asyncio.create_task(_gc.gc_collect())

    if conf.ap_mode: #begin wifi connection......
        from  my_app import WiFi
        w = WiFi()
        asyncio.create_task(w.wifi_ap_task(None,10))

    if conf.lora:
        from  lora_class import LoRa
        lora = LoRa()
        asyncio.create_task(lora.lora_receive_task(None,duration))

    if conf.beat_heart:
        beat_task = Multitask(3)
        asyncio.create_task(beat_task.beat())

    if conf.mqtt:
        mq = Multitask(10)
        asyncio.create_task(mq.mqtt())

    if conf.uart2:
        u = Multitask(5)
        asyncio.create_task(u.uart_send())

    if conf.modbus_tcp:
        t = Multitask(6)
        asyncio.create_task(t.modbustcp_send())

    #await asyncio.sleep(2)  # 加上这个，可以让不同的任务之间有5秒的间隔
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



