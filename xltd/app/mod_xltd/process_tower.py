# coding: utf-8
import requests,schedule,time,json

#memcache instance

def run_scheduled_task(**name):
    print('in xltd 塔吊数据--------------',name['mc_instance'])
    global mc_instance
    mc_instance = name['mc_instance']
    schedule.every(40).seconds.do(run_tower_data)

    while 1:
        schedule.run_pending()
        time.sleep(5)



def run_tower_data():
    _username = '中铁建工信联天地9-2-2地块项目'
    _pass = '123456'
    _url = 'https://www.safe110.net/API/Login.ashx?PostType=key&loginName={}&pwd={}'.format(_username, _pass)

    try:
        #step1 access tokenKen
        _r = requests.get(_url)
        _accessKey = _r.json()['rows']

        #step2 get ProjectID
        _url = 'https://www.safe110.net/API/API.ashx?PostType=GetEngineeringOrEquipmenttList&ForeignKey={}&UserName={}'.format(
            _accessKey, _username)
        _r = requests.get(_url)
        _projectid = _r.json()['rows'][0]['ProjectID']

        #step3 assemble devices
        _devices = []
        for d in _r.json()['rows']:
            _devices.append(d['DeviceSN'])

        #step4 获取塔吊基本信息
        _finaldata = {}

        for d in _devices:
            _url = 'https://www.safe110.net/API/API.ashx?PostType=GetTowerCraneLiveDataWithDriverInfo' \
                   '&ProjectID={}&DeviceSN={}&ForeignKey={}&UserName={}'.format(_projectid, d, _accessKey,
                                                                                _username)
            _r = requests.get(_url)
            _finaldata[d] = _r.json()['rows']

        print('final 塔吊数据 is =====', _finaldata)
        mc_instance.set('xltd_tower', json.dumps(_finaldata, ensure_ascii=False))

    except Exception as e:
        print('塔吊信息获取失败',e)



