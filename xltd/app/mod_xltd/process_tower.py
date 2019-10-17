# coding: utf-8
import requests,schedule,time,json,threading,memcache
#from app import  get_memcache

#memcache instance

def run_tower_scheduled_task(**name):
    print('in xltd 塔吊数据--------------',name['mc_instance'])
    global mc_instance
    mc_instance = name['mc_instance']
    #mc_instance = get_memcache()
    schedule.every(60).seconds.do(run_tower_data)

    while 1:
        schedule.run_pending()
        time.sleep(3)



def run_tower_data():
    _username = '中铁建工信联天地9-2-2地块项目'
    _pass = '123456'
    _url = 'https://www.safe110.net/API/Login.ashx?PostType=key&loginName={}&pwd={}'.format(_username, _pass)

    try:
        #step1 access tokenKen
        print('begin request=======================')
        _r = requests.get(_url)
        print("r.json is ==========",_r.json())
        _accessKey = _r.json()['rows']

        #step2 get ProjectID
        _url = 'https://www.safe110.net/API/API.ashx?PostType=GetEngineeringOrEquipmenttList&ForeignKey={}&UserName={}'.format(
            _accessKey, _username)
        _r = requests.get(_url)

        print('dddddddddddddddddddddd====',_r.json())
        _projectid = _r.json()['rows'][0]['ProjectID']
        print('projectID===================',_projectid)

        #step3 assemble devices
        _devices = []
        for d in _r.json()['rows']:
            _devices.append(d['DeviceSN'])

        print('devices=======================',_devices)

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
        print('塔吊信息获取失败11',e)


def get_memcache():
    return memcache.Client(['127.0.0.1:11211'], debug=True)

mc_instance = get_memcache()

t_tower_data = threading.Thread(target=run_tower_scheduled_task, kwargs={'mc_instance': mc_instance})
t_tower_data.start()

#run_tower_data()
