# -*- coding: UTF8 -*-
import config as conf
import uasyncio as asyncio

# if conf.sta_mode:
#     from my_app import WiFi
#     wifi = WiFi()
#     wifi.connect()

# if conf.ap_mode:
#     from my_app import WiFi
#     wifi = WiFi()
#     wifi.ap()

async def main_task(duration):
    from my_app import Multitask

    if conf.gc_collect:
        _gc = Multitask(600) #10分钟gc.collect()
        asyncio.create_task(_gc.gc_collect())

    if conf.lora_receive_mode:#true表明是数据接收网关，
        from  lora_class import LoRa
        lora = LoRa()
        lora.tr.setFrequency(conf.lora_receive_dict['frequency'])
        asyncio.create_task(lora.lora_receive_task(None,duration))

    if conf.beat_heart:
        beat_task = Multitask(conf.beat_heart_dict['interval'])
        asyncio.create_task(beat_task.beat())

    # if conf.mqtt:
    #     mq = Multitask(10)
    #     asyncio.create_task(mq.mqtt())
    #任何一个有效说明就是数据采集终端
    if conf.uart2 or conf.modbus_tcp:
        import modbus_task as m
        asyncio.create_task(m.main_task(20))

    while True:
        await asyncio.sleep(1)


def run(duration=20):
    try:
        asyncio.run(main_task(duration))
    except Exception as e:
        print('Interrupted',e)
    finally:
        asyncio.new_event_loop()
        print('asyncio run again.')

if conf.main_run:
    run()

