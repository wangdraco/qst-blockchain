# coding: utf-8
import requests,schedule,time,json,hashlib,base64

def run_scheduled_task(**name):
    print('in xltd 养护室温湿度数据--------------',name['mc_instance'])
    global mc_instance
    mc_instance = name['mc_instance']
    schedule.every(60).seconds.do(run_tower_data)

    while 1:
        schedule.run_pending()
        time.sleep(5)



def run_tower_data():

    #step 1 ,加密签名 对 appid=APPID&nonce=jashbdjbjsdbjasfd&timestamp=1544155195&key=APPSECRET 进行md5
    _appid = 'wlzk3ddfc526d5f4066f7566369a37e4'
    _key = 'c63754186f1ab57d2484461012c10b36'
    _nonce = 'abcd'
    _s = 'appid={}&nonce={}&timestamp={}&key={}'.format(_appid,_nonce,
        str(time.time()),_key)
    _md5 = hashlib.md5(_s.encode()).hexdigest()


    try:
        # step2 得到 token
        url = 'http://cloud.husin.cn/open/v1/access_token'
        payload = {'appid': _appid,
                   'nonce': _nonce,
                   'timestamp': str(time.time()),
                   'sign': _md5}
        r = requests.post(url, json=payload)
        print(r.content.decode())
        _token = r.json()['data']['access_token']
        _uid = r.json()['data']['client']['uid']
        _user_id = r.json()['data']['client']['user_id']

        #step3 得到设备id, 通过http://cloud.husin.cn/open/v1/device_list 接口
        _device_list = 'http://cloud.husin.cn/open/v1/device_list'
        #在header 中进行authorization 字段拼接，拼接规则：authorization:USERID base64_encode(appid:access_token:uid:user_id)
        _base = base64.b64encode(('{}:{}:{}:{}'.format(_appid,_token,_uid,_user_id)).encode('utf-8'))
        _authdata = 'USERID {}'.format(str(_base, 'utf-8'))
        headers = {'Authorization': _authdata}
        payload = {'page': '1'}


        #得到的结果是id=161，可以写死在程序里
        #r = requests.post(_device_list, json=payload, headers=headers)
        #print(r.content.decode(encoding='utf-8'))

        #step4 得到设备详情，里面有设备对应的值 ,接口http://cloud.husin.cn/open/v1/device_info?id=161&from=info
        _dataurl = 'http://cloud.husin.cn/open/v1/device_info?id=161&from=info'
        r = requests.get(_dataurl, headers=headers)
        print(r.json())
        _data = r.json()['data']['bases']

        _result = {}
        for d in _data:
            if d['biaoshi'] == 'wendu':
                _result['temperature'] = str(d['value']).replace(d['unit'],'')
            if d['biaoshi'] == 'shidu':
                _result['humidity'] = str(d['value']).replace(d['unit'],'')
                _result['dataTime'] = d['time']
                _result['status'] = '正常'

        mc_instance.set('xltd_room', json.dumps(_result, ensure_ascii=False))
        print('final================',_result)


    except Exception as e:
        print('养护室读取温湿度出错',e)

