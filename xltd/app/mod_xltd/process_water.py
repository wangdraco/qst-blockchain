# coding: utf-8
import requests,schedule,time,json

#如果都是在同一台机器上部署的，就不需要单独的部署程序了，因为使用的同一个memcache
#这个文件的目的是处理那些连接困难的gprs客户端，从长连接中获取socket

def run_scheduled_task(**name):
    print('in xltd long connect water--------------',name['mc_instance'])
    global mc_instance
    mc_instance = name['mc_instance']
    schedule.every(38).seconds.do(run_water_data)

    while 1:
        schedule.run_pending()
        time.sleep(5)



def run_water_data():


    try:
        _data = {}
        _command = [0x01,0x03,0x02,0x02,0x00,0x02,0x64,0x73]

        mc_instance.set('xltd_electronic', json.dumps(_data, ensure_ascii=False))

    except Exception as e:
        print('取水表数据出错',e)


    print('final 水表 data is =====', _data)
