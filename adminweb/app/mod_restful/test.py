import requests,json

def access_token():

    _posturl = 'http://127.0.0.1:8091/token/access'

    # 根据client_id和 client_secret生成token，验证的时候从 client_list.json里得到这两个值再加valid是否有效标志进行验证
    _payload = {'client_id': 3001, 'client_secret': '56ce7e80-5939-443f-b733-ea7b2175fe68', 'scope': 'public_web_api'}

    # post 提交数据有三种 常用的是form表单提交，就是下面的这种，如果是application/json 则是以json格式提交数据，参数就是json=_payload
    r = requests.post(url=_posturl, headers={"ContentType": "application/x-www-form-urlencoded"}, data=_payload)
    print(r.headers)
    print(r.json())
    return r.json()

def getUserList():
    _geturl = 'http://127.0.0.1:8091/getdata'
    # _token = json.loads(access_token())
    _token = 'eyJhbGciOiJIUzI1NiIsImlhdCI6MTU5NjA5ODg0MSwiZXhwIjoxNTk2MDk4OTYxfQ.eyJjbGllbnRfaWQiOjMwMDEsImNsaWVudF9zZWNyZXQiOiI1NmNlN2U4MC01OTM5LTQ0M2YtYjczMy1lYTdiMjE3NWZlNjgiLCJzY29wZSI6InB1YmxpY193ZWJfYXBpIn0.sakyFF1S5zPoXbtwycixs34bx0F4EpiyRilV4GNX3u8'
    headers = {'Authorization': f'Bearer {_token}'}
    r = requests.get(_geturl,headers=headers)
    print(r.headers)
    print(r.json())

#access_token()
getUserList()