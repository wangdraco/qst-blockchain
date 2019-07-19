# coding: utf-8
import requests,schedule,time,json

#memcache instance

def run_scheduled_task(**name):
    print('in xltd dust--------------',name['mc_instance'])
    global mc_instance
    mc_instance = name['mc_instance']
    schedule.every(20).seconds.do(run_dustdata)

    while 1:
        schedule.run_pending()
        time.sleep(5)



def run_dustdata():
    _url = 'http://www.0531yun.cn/wsjc/Device/getDeviceData.do?userID=181226jnwj&userPassword=181226jnwj'
    _key = '40034083'

    try:
        _data = {}
        r = requests.get(_url)

        for i in r.json():
            if i['DevAddr'] == _key and i['devPos'] == '1':
                _data['pm10'] = i['DevTempValue']
                _data['pm25'] = i['DevHumiValue']

            if i['DevAddr'] == _key and i['devPos'] == '2':
                _data['noise'] = i['DevHumiValue']

            if i['DevAddr'] == _key and i['devPos'] == '3':
                _data['temp'] = i['DevTempValue']
                _data['humidity'] = i['DevHumiValue']

            if i['DevAddr'] == _key and i['devPos'] == '4':
                _data['speed'] = i['DevHumiValue']

            if i['DevAddr'] == _key and i['devPos'] == '5':
                _data['direction'] = i['DevTempValue']

        mc_instance.set('xltd_dust', json.dumps(_data, ensure_ascii=False))

    except Exception:
        print(Exception,mc_instance.get('xltd_dust'))


    print('final dust data is =====', _data)
