# coding: utf-8
import requests,schedule,time,json
from app import get_memcache

#如果都是在同一台机器上部署的，就不需要单独的部署程序了，因为使用的同一个memcache

def run_scheduled_task(**name):
    print('in xltd electronic--------------',name['mc_instance'])
    global mc_instance
    #mc_instance = name['mc_instance']
    mc_instance = get_memcache()
    schedule.every(38).seconds.do(run_elec_data)

    while 1:
        schedule.run_pending()
        time.sleep(5)



def run_elec_data():
    #项目部用电
    project_url = 'http://139.129.200.70:5000/device/db-9197,12,50'

    #现场东
    east_url = 'http://139.129.200.70:5000/device/db-9195,12,50'
    # 现场北
    north_url = 'http://139.129.200.70:5000/device/db-9192,12,50'

    # 生活区北
    living_north_url = 'http://139.129.200.70:5000/device/db-9196,12,50'

    try:
        _data = {}
        r1 = requests.get(project_url)
        _data['project_data'] = r1.json()['db-9197-12']

        # r2 = requests.get(east_url)
        # _data['east_data'] = r2.json()['db-9195-12']

        r3 = requests.get(north_url)
        _data['north_data'] = r3.json()['db-9192-12']

        r4= requests.get(living_north_url)
        _data['living_north_data'] = r4.json()['db-9196-12']

        mc_instance.set('xltd_electronic', json.dumps(_data, ensure_ascii=False))

    except Exception as e:
        print('取电表数据出错',e)


    print('final 电表 data is =====', _data)
