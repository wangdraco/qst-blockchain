from microdot import Microdot, Response,send_file,redirect
import time,json
import config as conf
app = Microdot()


@app.route('/web/<path:path>')
def response_web_resource(request,path):

    response = send_file('web/'+path)
    return response

@app.route('jquery-ui.css')
def response_jquery_ui_css(request):

    response = send_file('jquery-ui.css')
    return response

@app.route('jquery-3.5.1.min.js')
def response_jquery_min_js(request):

    response = send_file('jquery-3.5.1.min.js')
    return response

@app.route('jquery-ui.min.js')
def response_jquery_ui_js(request):

    response = send_file('jquery-ui.min.js')
    return response

@app.route('/index', methods=['GET', 'POST'])
def response_index(request):
    if request.method == 'POST':
        pass
    else:
        if request.cookies and "admin&123" in request.cookies['user_cookies']:
            response = send_file('index.html')
        else:
            response = redirect("/")
        return response

@app.route('/main.css', methods=['GET'])
def response_css(request):

    response = send_file('main.css')
    return response


@app.route('/main', methods=['GET', 'POST'])
def main(request):
    if request.method == 'POST':
        pass
    else:
        if "admin&123" in request.cookies['user_cookies']:
            response = send_file('main.html')
        else:
            response = redirect("/")
        return response



@app.route('/', methods=['GET', 'POST'])
def index(request):
    user_cookies = None
    message_cookie = None
    machine_cookie = None
    response = None
    if request.method == 'POST':
        _u = request.form["username"]
        _p = request.form["password"]

        if _u == conf.web_username and _p == conf.web_password:
            response = redirect("/index")
            user_cookies = "{}&{}".format(_u, _p)
            machine_cookie = conf.mac_id
            response.set_cookie('ssid_c', conf.SSID)
            response.set_cookie('wifi_c', conf.PASSWORD)

        else:
            response = send_file('login.html')
            message_cookie = "{}&{}".format('用户名', '密码错误')
            response.set_cookie('message', message_cookie)
            return response
    else:
        response = send_file('login.html')
        response.set_cookie('message', "")
        response.set_cookie('user_cookies', "")


    if message_cookie:
        response.set_cookie('message', message_cookie)
    if user_cookies:
        response.set_cookie('user_cookies', user_cookies)
    if machine_cookie:
        response.set_cookie('machine_cookies', machine_cookie)

    return response

htmldoc = """<!DOCTYPE html>
<html>
    <head>
        <title>Microdot Example Page</title>
        <link rel="stylesheet"  href="bootstrap.css" crossorigin="anonymous">
    </head>
    <body>
        <div>
            <h1>Microdot Example Page</h1>
            <p>Hello from Microdot!</p>
        </div>
    </body>
</html>
"""

@app.route("/post/connect/wifi", methods=["POST"])
def connect_wifi(request):
    _response = json.loads(request.body.decode())
    _ssid = _response["ssid"]
    _p = _response["wifipassword"]
    _result = {}
    _result['connected'] = 'False'
    # from wifi_class import WiFi
    # wifi = WiFi(ssid=_ssid, password=_p)
    # _sta = wifi.connect()
    #
    # start = time.time()
    #
    # while time.time() < start + 30:
    #     time.sleep(1)
    #     print('wifi connecting......,', _sta.ifconfig())
    #     if _sta.isconnected():
    #         _result['connected'] = 'True'
    #         break

    #return "ssss"
    return Response(body=_result, headers={"Content-Type": "application/json"})

@app.route("/post/save/wifi", methods=["POST"])
def save_wifi(request):
    _response = json.loads(request.body.decode())
    _ssid = _response["ssid"]
    _p = _response["wifipassword"]

    alter('config.py',"SSID = ", "'{}'".format(_ssid))
    alter('config.py', "PASSWORD = ", "'{}'".format(_p))

    return Response(body={'connected':'True'}, headers={"Content-Type": "application/json"})

@app.route("/post/connect/modbus", methods=["POST"])
def connect_modbus(request):
    _response = json.loads(request.body.decode())
    _ip = str(_response["slaveip"])
    _port = int(_response["slaveport"])
    _slaveaddr = int(_response["slaveaddr"])
    _startaddr = int(_response["startaddr"])
    _readquantity = int(_response["readquantity"])
    _ft03 = _response["ft03"]
    _ft02 = _response["ft02"]

    _result = {}
    _result['connected'] = 'True'
    from modbus_class import modbus
    try:
        m = modbus(_slaveaddr, _startaddr, _readquantity)
        m.modbus_tcp(_ip, _port)
        if _ft03:
            _result['data'] = str(m.read_holding_registers())
        if _ft02:
            _result['data'] = str(m.read_discrete_inputs())
    except Exception as e:
        print(e)
        _result['connected'] = 'False'


    return Response(body=_result, headers={"Content-Type": "application/json"})

@app.route("/post/connect/modbus_rtu", methods=["POST"])
def connect_modbus_rtu(request):
    _response = json.loads(request.body.decode())
    _baundrate = int(_response["baundrate"])
    _rtu_slaveaddr = int(_response["rtu_slaveaddr"])
    _rtu_startaddr = int(_response["rtu_startaddr"])
    _rtu_readquantity = int(_response["rtu_readquantity"])
    _fr03 = _response["fr03"]
    _fr02 = _response["fr02"]

    _result = {}
    _result['connected'] = 'True'
    from modbus_class import modbus
    try:
        m = modbus(_rtu_slaveaddr, _rtu_startaddr, _rtu_readquantity)
        m.modbus_serial(_baundrate)
        if _fr03:
            _result['data'] = str(m.read_holding_registers())
        if _fr02:
            _result['data'] = str(m.read_discrete_inputs())
    except Exception as e:
        print(e)
        _result['connected'] = 'False'


    return Response(body=_result, headers={"Content-Type": "application/json"})

#alter config.py file
def alter(file,key_str,value_str):
    file_data = ""
    with open(file, "r", encoding="utf-8") as f:
        for line in f:
            if key_str in line:
                #line.partition(old_str) #return key_str
                line = key_str + value_str +"\n"
            file_data += line

    with open(file, "w", encoding="utf-8") as f:
        f.write(file_data)
# app.run(debug=True)