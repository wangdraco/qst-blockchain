from flask import Flask, request
from flask_restful import reqparse, abort, Api, Resource
import requests

app = Flask(__name__)

api = Api(app)


# parser = reqparse.RequestParser()
'''
access token ,using case :
_posturl = 'http://139.129.200.70:8091/token/api/connect/token'
_payload = {'client_id': 3001, 'client_secret': '56ce7e80-5939-443f-b733-ea7b2175fe68', 'scope': 'office_web_api',
            'grant_type': 'client_credentials'}
# post 提交数据有三种 常用的是form表单提交，就是下面的这种，如果是application/json 则是以json格式提交数据，参数就是json=_payload
r = requests.post(url=_posturl, headers={"ContentType": "application/x-www-form-urlencoded"}, data=_payload)
print(r.json())
'''
class AccessToken(Resource):

    def post(self):
        # 得到form表单提交过来的数据
        print(request.form["client_secret"])

        # 对传过来的数据进行验证
        parse = reqparse.RequestParser()
        parse.add_argument('client_id', trim=True, choices=[3001], type=int, default=3001, help='client_id验证错误')
        parse.add_argument('client_secret', type=str, choices=['56ce7e80-5939-443f-b733-ea7b2175fe68'],
                           help='client_secret不对')
        parse.add_argument('scope', type=str, choices=['office_web_api'], help='scope没有可选项')
        parse.add_argument('grant_type', type=str, choices=['client_credentials'], help='grant_type验证错误', required=True)

        args = parse.parse_args()

        # 从智家平台上拿数据
        _posturl = 'https://idoffice.zhijiaiot.com/connect/token'
        _payload = {'client_id': args.get('client_id'), 'client_secret': args.get('client_secret'),
                    'scope': args.get('scope'), 'grant_type': args.get('grant_type')}
        print('_payload is ', _payload)
        r = requests.post(url=_posturl, headers={"ContentType": "application/x-www-form-urlencoded"}, data=_payload)

        return r.json()


class DeviceList(Resource):

    def post(self):
        print(request.headers['Authorization'])

        headers = {'Authorization': request.headers['Authorization'],
                   "ContentType": "application/x-www-form-urlencoded"}

        # 对传过来的数据进行验证
        parse = reqparse.RequestParser()
        parse.add_argument('projectId', type=str, choices=['ce35d6ef-18d3-43bc-ad6f-c58ad159be7e'], required=True,
                           help='projectId不对')
        parse.add_argument('original', type=int, choices=[0, 1], help='original不对')
        args = parse.parse_args()

        # 从智家平台上拿数据
        # devicelist = 'https://apioffice.zhijiaiot.com/api/ClientDevice/List'
        # _payload = {'projectId': args.get('projectId')}
        # request_device = requests.post(devicelist, headers=headers, data=_payload)


        # 从智家平台上拿数据
        headers = {'Authorization': request.headers['Authorization'],
                   "ContentType": "application/json;charset=UTF-8"}
        devicelist = 'https://apioffice.zhijiaiot.com/api/ClientDevice/List' + f'?projectId={args.get("projectId")}' + f'&original={args.get("original")}'

        request_device = requests.post(devicelist, headers=headers)

        return request_device.json()


class OperateDevice(Resource):
    def post(self):
        print(request.headers['Authorization'])

        headers = {'Authorization': request.headers['Authorization'],
                   "ContentType": "application/json;charset=UTF-8"}
        _jsondata = request.json
        print('get json data is ===', _jsondata)

        # 对传过来的数据进行验证
        parse = reqparse.RequestParser()
        parse.add_argument('device_id', type=str, required=True, help='device_id不对')
        parse.add_argument('services', required=True, type=dict)
        args = parse.parse_args()

        # 还可以对嵌套的数据进行验证
        nested_one_parser = reqparse.RequestParser()
        nested_one_parser.add_argument('switch', type=int, choices=[0, 1, 2], location=('services',),
                                       help='switch参数不对')
        nested_one_parser.add_argument('ir', type=dict, location=('services',))
        nested_one_args = nested_one_parser.parse_args(req=args)

        # 向智家平台上发送数据
        devicelist = 'https://apioffice.zhijiaiot.com/api/ClientDevice/Invoke'

        if nested_one_args.get('ir') is None:  # 开关插座的控制操作

            _payload = {'device_id': args.get('device_id'), 'services': {'switch': _jsondata['services']['switch']}}

        else:
            _payload = {'device_id': args.get('device_id'),
                        'services': {'ir': {'code': _jsondata['services']['ir']['code']}}}

        print('final 控制payload is ==========', _payload)
        request_device = requests.post(devicelist, headers=headers, json=_payload)

        return request_device.json()



#获取红外码
class IrDeviceCode(Resource):
    def post(self):

        _jsondata = request.args
        print('get 红外线遥控器 json data is ===', _jsondata)

        # 从智家平台上拿数据
        headers = {'Authorization': request.headers['Authorization'],
                   "ContentType": "application/json;charset=UTF-8"}
        ircode = 'https://apioffice.zhijiaiot.com/api/ClientDevice/GetIrCodes' + f'?device_id={args.get("device_id")}'

        request_device = requests.post(ircode, headers=headers)

        return request_device.json()


#接收事件通知
class EventNotify(Resource):
    def post(self):
        headers = {"ContentType": "application/json"}

        _jsondata = request.json
        print('得到的事件数据是 ==== ===', _jsondata)

        #write to memcache
        if _jsondata.get('services')['on_off']:
            print(_jsondata.get('device_id'))


api.add_resource(AccessToken, '/token/api/connect/token')
api.add_resource(DeviceList, '/api/ClientDevice/List')
api.add_resource(OperateDevice,'/api/ClientDevice/Invoke')
api.add_resource(IrDeviceCode,'/api/ClientDevice/GetIrCodes')
api.add_resource(EventNotify,'/api/event/Notify')

if __name__ == "__main__":
    app.run(host='139.129.200.70', port=8091, debug=True)
