# coding: utf-8
import requests,datetime,json
from werkzeug.utils import secure_filename

# payload = {'id':0,'event_desc':'与义工交互4','event_type':2,'event_date':datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#            ,'event_location':'室外','oldperson_id':3}
#
# r = requests.post('http://127.0.0.1:5000/datamanage/api/insertevent', json=payload)

#r = requests.get('http://127.0.0.1:5000/testauth',auth=('manager', '1q'))

# r = requests.get('http://www.0531yun.cn/wsjc/Device/getDeviceData.do?userID=181226jnwj&userPassword=181226jnwj')
# print(r.json())
# for i in r.json():
#     if i['DevAddr'] == '40030330' and i['devPos'] == '1':
#         print(i['DevKey'],'---',i['DevTempValue'],'-----',i['DevHumiValue'])
#         break


#测试 Authorization
def test_auth():
    headers = {'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsImlhdCI6MTU5NTA4NTE4MCwiZXhwIjoxNTk1MDg1MjQwfQ.eyJ1c2VybmFtZSI6IkpvaG4xMSJ9.28-GJy-boSFbxaq6JSr5akbeoXWifVI6Avgs8Zvhs60'}
    r = requests.get('http://127.0.0.1:5000/device/water/presure/24', headers=headers)
    print(r.json())

# r = requests.get('http://smart.iotdatatech.net/device/water/presure/24', headers=headers)
# r.headers['Authorization'] ='Bearer secret-token-1'
#print(r.headers.values(), r.json())

#tower crane realtime data
# _projectid = 'ae676605-72b2-e811-bcba-d094662ce243'
# _devicesn = '010818080297'
# _foreignkey = '268a1433-ee47-49a2-86bc-6ed910a4296c'
# _username = '中铁建工日照秦家楼项目'
#
# r = requests.get('https://www.safe110.net/API/API.ashx?PostType=GetTowerCraneLiveDataWithDriverInfo'
#                  '&ProjectID={}&DeviceSN={}&ForeignKey={}&UserName={}'.format(_projectid,_devicesn,_foreignkey,_username))
# print(r.json())
# print(secure_filename('d:/3434/dd.html'))

#测试烟台公共资源中心中控项目
#测试 Authorization
#登录与鉴权
def access_token():
    _posturl = 'https://idoffice.zhijiaiot.com/connect/token'
    _posturl = 'http://139.129.200.70:8091/token/api/connect/token'

    _payload = {'client_id': 3001, 'client_secret': '56ce7e80-5939-443f-b733-ea7b2175fe68', 'scope': 'office_web_api',
                'grant_type': 'client_credentials'}

    # post 提交数据有三种 常用的是form表单提交，就是下面的这种，如果是application/json 则是以json格式提交数据，参数就是json=_payload
    r = requests.post(url=_posturl, headers={"ContentType": "application/x-www-form-urlencoded"}, data=_payload)
    print(r.json())


#读取设备列表
def device_list():
    headers = {'Authorization': 'Bearer 62e2bafd86900ffc0d1ae1fe8aa72eff43a51abe33a0b59d0cf1b6addcfc3456',"ContentType": "application/x-www-form-urlencoded;charset=UTF-8"}
    #devicelist = 'https://apioffice.zhijiaiot.com/api/ClientDevice/List'
    devicelist = 'http://139.129.200.70:8091/api/ClientDevice/List'
    _payload = {'projectId':'ce35d6ef-18d3-43bc-ad6f-c58ad159be7e','original':1}


    request_device = requests.post(devicelist, headers=headers, data=_payload)
    print(request_device.json())

#d
def device_list_new():
    headers = {'Authorization': 'Bearer 62e2bafd86900ffc0d1ae1fe8aa72eff43a51abe33a0b59d0cf1b6addcfc3456',
               "ContentType": "application/json"}

    # request_device = requests.post(devicelist, headers=headers, data=_payload)
    _payload = {'projectId': 'ce35d6ef-18d3-43bc-ad6f-c58ad159be7e','original':0}
    devicelist = 'https://apioffice.zhijiaiot.com/api/ClientDevice/List' + f'?projectId={_payload["projectId"]}'+f'&original={_payload["original"]}'
    print('=====,',devicelist)
    r = requests.post(devicelist, headers=headers)
    print(r.json())

#获取单个设备
def get_device():
    headers = {'Authorization' : 'Bearer 62e2bafd86900ffc0d1ae1fe8aa72eff43a51abe33a0b59d0cf1b6addcfc3456',"ContentType": "application/x-www-form-urlencoded"}
    device =  'https://apioffice.zhijiaiot.com/api/ClientDevice/Get'
    _payload = {'device_id':'------------'}
    r =  requests.post(device, headers=headers, data=_payload)
    print(r.json())

#控制单个设备，开关或插座
def operate_device():
    headers = {'Authorization' : 'Bearer 62e2bafd86900ffc0d1ae1fe8aa72eff43a51abe33a0b59d0cf1b6addcfc3456',"ContentType": "application/json;charset=UTF-8"}
    device =  'https://apioffice.zhijiaiot.com/api/ClientDevice/Invoke'
    #device = 'http://139.129.200.70:8091/api/ClientDevice/Invoke'
    _payload = {"device_id":"5f17deef883ec940a8fc2e71@1","services":{"switch":1}}
    r =  requests.post(device, headers=headers, json=_payload)
    print(r.json())


#控制红外设备
def operate_ir_device():
    headers = {'Authorization' : 'Bearer 62e2bafd86900ffc0d1ae1fe8aa72eff43a51abe33a0b59d0cf1b6addcfc3456',"ContentType": "application/json;charset=UTF-8"}
    device =  'https://apioffice.zhijiaiot.com/api/ClientDevice/Invoke'
    #device = 'http://139.129.200.70:8091/api/ClientDevice/Invoke'
    _payload = {"device_id":"5f192a1a57ef6730f0dfe19e",
                "services":{"ir":{"code":"3003596300347f4b070021011801240021006a002000530b20008417230000001f00ffffffff01233322222333222222332222332233334135135135135136f0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000003763e2e"}}}
    r =  requests.post(device, headers=headers, json=_payload)
    print(r.json())

#测试获取红外码的api
def get_ir_code():
    headers = {'Authorization': 'Bearer 62e2bafd86900ffc0d1ae1fe8aa72eff43a51abe33a0b59d0cf1b6addcfc3456',
               "ContentType": "application/json;charset=UTF-8"}
    # device = 'http://139.129.200.70:8091/api/ClientDevice/GetIrCodes?device_id=5f19412b3d14ed2500ae9102'

    device = 'http://139.129.200.70:8091/api/ClientDevice/GetIrCodes'
    _payload = {'device_id':'5f19412b3d14ed2500ae9102'}

    #params means the queryString parameters, like /GetIrCodes?device_id=5f19412b3d14ed2500ae9102
    r = requests.post(device, headers=headers,params=_payload)
    print(r.json())


#测试通知事件
def event_notify():
    headers = {"ContentType": "application/json"}
    event_url = 'http://139.129.200.70:8091/api/event/Notify'
    _payload = {"device_id": "5f17da79883ec940a8fc2e70", "services": {"port_on_off": [0,1,2,4]}}
    r = requests.post(event_url, headers=headers, json=_payload)
    print(r)

#device_list()

#test_auth()

operate_device()
#operate_ir_device()
#event_notify()
#get_ir_code()
#device_list_new()
# headers = {'Authorization': 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6IkpvaG4xMSJ9._kWlCBIsJ2dHDlKr0z6M--fjraPwXmJAeapJznSS23c'}
# r = requests.get('http://127.0.0.1:5000/device/water/presure/24', headers=headers)