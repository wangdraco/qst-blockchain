from itsdangerous import TimedJSONWebSignatureSerializer as Serializer,SignatureExpired,BadSignature
from flask import Flask,jsonify
from flask_restful import reqparse, abort, Api, Resource
import requests,json
from flask_httpauth import HTTPTokenAuth


app = Flask(__name__)

api = Api(app)

serializer = Serializer('salt', expires_in=120,algorithm_name='HS256')  # 60 seconds
class GenerateToken(Resource):

    def post(self):

        # 对传过来的数据进行验证
        parse = reqparse.RequestParser()
        parse.add_argument('client_id', trim=True,  type=int, required=True, help='client_id验证错误')
        parse.add_argument('client_secret', type=str,required=True,help='client_secret不对')
        parse.add_argument('scope', type=str, choices=['public_web_api'], required=True, help='scope没有可选项')
        args = parse.parse_args()

        _payload = {'client_id': args.get('client_id'), 'client_secret': args.get('client_secret'),
                    'scope': args.get('scope')}
        print('_payload is ', _payload)

        #根据传递过来的form data ，生成token数据,第一个参数是secret_key

        token = serializer.dumps(_payload)
        s_token = str(token,encoding="utf-8")
        print(f'final token is ================={s_token}')
        _result = {}
        # _result['token'] = s_token[:50]+""+s_token[-50:]
        _result['token'] = s_token
        _result['expires_in'] = 120
        _result['token_type'] = "Bearer"
        _result['scope'] = 'public_web_api'

        return json.dumps(_result)

# api.add_resource(GenerateToken, '/token/access')
def make_resources():
    api.add_resource(GenerateToken, '/token/access')


#验证真实数据的有效性,用clientID和 clientSecret，还有status三个字段验证解码后的token是否正确
def verify_client_data(clientId,clientSecret):
    isValid = False
    _list = json.load(open("client_list.json"))
    for d in _list['clients']:
        if d['status'] == 'valid':
            print(type(d.values()))
            if clientId in d.values() and clientSecret in d.values():
                print('yes')
                isValid = True
                break

    return isValid


#api token authentication
auth = HTTPTokenAuth(scheme='Bearer')

'''
在需要auth验证的方法上加 
@auth.login_required 就可以了
系统自动调用下面的@auth.verify_token方法
'''

@auth.verify_token
def verify_token(token):
    print(f'begin authentication.......{token}')
    try:
        data = serializer.loads(token)
        print(f'token is {token} and the after loads ,data is {data}')
    except SignatureExpired:
        print('valid token, but expired!!!!!')
        global error_msg
        error_msg = 'token expired'
        return False  # valid token, but expired
    except BadSignature:
        error_msg = 'invalid token!!!!!!!!!!!!!'
        print(error_msg)
        return False  # invalid token

    #根据实际数据,验证token的有效性
    if verify_client_data(data['client_id'],data['client_secret']):
    #if '56ce7e80-5939-443f-b733-ea7b2175fe68' == data['client_secret']:
        print('Authentication is succeed !!!!!!!', data)
        return True
    return False

@app.route('/getdata')
@auth.login_required
def getdata():
    return json.dumps({"name":"andy"}),200


#重要： json.dumps返回的Content-Type=text/html，而jsonify返回的是application/json
@auth.error_handler
def auth_error(status):
    return jsonify({'error': error_msg}),status

if __name__ == "__main__":
    # verify_client_data(3001,'56ce7e80-5939-443f-b733-ea7b2175fe68')

    make_resources()
    app.run(host='127.0.0.1', port=8091, debug=True)