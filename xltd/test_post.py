import requests,hashlib,datetime,time,base64

# #济南互信智能 gprs温湿度传感器
# _s = 'appid=wlzk3ddfc526d5f4066f7566369a37e4&nonce=abcd&timestamp={}&key=c63754186f1ab57d2484461012c10b36'.format(str(time.time()))
# _md5 = hashlib.md5(_s.encode()).hexdigest()
# print('md5------------',_md5)
#
# url = 'http://cloud.husin.cn/open/v1/access_token'
# payload ={'appid':'wlzk3ddfc526d5f4066f7566369a37e4',
#           'nonce':'abcd',
#           'timestamp':str(time.time()),
#           'sign':_md5}
#
# r = requests.post(url, json=payload)
# #print(r.content.decode(encoding='utf-8'))
# print(r.content.decode())
# _token = r.json()['data']['access_token']
# print(_token)
# _dataurl = 'http://cloud.husin.cn/open/v1/device_list'
#
# payload = {'page':'1'}
#
# _base = base64.b64encode(('wlzk3ddfc526d5f4066f7566369a37e4:{}:348:0'.format(_token)).encode('utf-8'))
# _authdata = 'USERID {}'.format(str(_base,'utf-8'))
# print(_authdata)
# headers = {'Authorization': _authdata}
#
# #add device
# #_dataurl = 'http://cloud.husin.cn/open/v1/add_device'
# #payload = {'device_name':'信联天地养护室'}
#
# r = requests.post(_dataurl, json=payload , headers=headers)
# print(r.content.decode(encoding='utf-8'))
#
# _dataurl = 'http://cloud.husin.cn/open/v1/device_info?id=161&from=info'
# payload = {'id':161}
# r = requests.get(_dataurl,  headers=headers)
# print(r.json())






# headers = {'Authorization': 'USERID 9a47dff0bd85fa573c72557e18fe15f9'}
# r = requests.get('http://cloud.husin.cn/open/v1/access_token', headers=headers)
# print(r.json())

# url = 'http://192.168.0.112:8090/face/find'
# payload = {'pass':'12345678','personId':''}
# r = requests.post(url, json=payload)
# print(r.json())

#ta diao
_username = '中铁建工信联天地9-2-2地块项目'
_pass = '123456'
_url = 'https://www.safe110.net/API/Login.ashx?PostType=key&loginName={}&pwd={}'.format(_username,_pass)
_r = requests.get(_url)
print(_r.json())
_accessKey = _r.json()['rows']
print(_accessKey)

#获取用户下的工程和设备

_url = 'https://www.safe110.net/API/API.ashx?PostType=GetEngineeringOrEquipmenttList&ForeignKey={}&UserName={}'.format(_accessKey,_username)

_r = requests.get(_url)
print(_r.json())

_projectid = _r.json()['rows'][0]['ProjectID']
print(_projectid)

_devices = []
for d in _r.json()['rows']:
    _devices.append(d['DeviceSN'])

print(_devices)

#获取塔吊基本信息
_url = 'https://www.safe110.net/API/API.ashx?PostType=GetTowerCraneLiveDataWithDriverInfo' \
       '&ProjectID={}&DeviceSN={}&ForeignKey={}&UserName={}'.format(_projectid,'010819050048',_accessKey,_username)

_r = requests.get(_url)
print(_r.json())

_finaldata = {}

for d in _devices:
    _url = 'https://www.safe110.net/API/API.ashx?PostType=GetTowerCraneLiveDataWithDriverInfo' \
           '&ProjectID={}&DeviceSN={}&ForeignKey={}&UserName={}'.format(_projectid, d, _accessKey,
                                                                        _username)
    _r = requests.get(_url)
    _finaldata[d] = _r.json()['rows']

print('final 塔吊数据============',_finaldata)
