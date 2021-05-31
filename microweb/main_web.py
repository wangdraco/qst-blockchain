from microdot import Microdot, Response,send_file,redirect
import json,time
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
            response.set_cookie('frequency', conf.lora_frequency)
            response.set_cookie('baundrate', conf.uart2_dict['baudrate'])
            response.set_cookie('mqttip', conf.mqtt_dict["broker_address"])
            response.set_cookie('mqttport', conf.mqtt_dict["broker_port"])
            response.set_cookie('mqtttopic', conf.mqtt_dict["topic"].decode())
            response.set_cookie('mqttuser', "" if conf.mqtt_dict["mqtt_user"] is None else conf.mqtt_dict["mqtt_user"])
            response.set_cookie('mqttpassword', "" if conf.mqtt_dict["mqtt_password"] is None else conf.mqtt_dict["mqtt_password"])
            response.set_cookie('sta_mode', str(conf.sta_mode))
            response.set_cookie('uart2', str(conf.uart2))
            response.set_cookie('modbus_tcp', str(conf.modbus_tcp))
            response.set_cookie('enable_lora', str(conf.lora))
            response.set_cookie('enable_mqtt', str(conf.mqtt))
            response.set_cookie('enable_heart', str(conf.beat_heart))
            response.set_cookie('lora_receive_mode', str(conf.lora_receive_mode))
            response.set_cookie('lora_receive_freq', str(conf.lora_receive_dict["frequency"]))
            response.set_cookie('lora_receive_mqtt', str(conf.lora_receive_dict["mqtt"]))
            response.set_cookie('lora_receive_uart', str(conf.lora_receive_dict["uart2"]))

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


@app.route("/post/reboot", methods=["POST"])
def reboot_device(request):
    _result = {}
    _result['connected'] = 'False'
    try:
        import reboot_task
        _result['connected'] = 'True'
    except:
        pass
    # return "ssss"
    return Response(body=_result, headers={"Content-Type": "application/json"})

@app.route("/post/init", methods=["POST"])
def init_device(request):
    _result = {}
    _result['connected'] = 'False'
    try:
        init_config('config.py', 'config_init.py')
        time.sleep(0.5)
        import reboot_task
        _result['connected'] = 'True'
    except:
        pass

    return Response(body=_result, headers={"Content-Type": "application/json"})

@app.route("/post/connect/wifi", methods=["POST"])
def connect_wifi(request):
    _response = json.loads(request.body.decode())
    _ssid = _response["ssid"]
    _p = _response["wifipassword"]
    _result = {}
    _result['connected'] = 'False'
    from wifi_class import WiFi
    wifi = WiFi(ssid=_ssid, password=_p)
    _sta = wifi.connect()

    start = time.time()

    while time.time() < start + 30:
        time.sleep(1)
        print('wifi connecting......,', _sta.ifconfig())
        if _sta.isconnected():
            _result['connected'] = 'True'
            break

    #return "ssss"
    return Response(body=_result, headers={"Content-Type": "application/json"})

@app.route("/post/save/wifi", methods=["POST"])
def save_wifi(request):
    _response = json.loads(request.body.decode())
    _ssid = _response["ssid"]
    _p = _response["wifipassword"]
    _enable = _response["enable_wifi"]
    _disable = _response["disable_wifi"]
    _result = True
    if _enable: _result=True
    if _disable: _result = False

    alter('config.py', "sta_mode = ", "{}".format(_result))
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


@app.route("/post/save/modbus", methods=["POST"])
def save_modbus(request):
    _response = json.loads(request.body.decode())
    _device = str(_response["device_no"])
    _ip = str(_response["slaveip"])
    _port = int(_response["slaveport"])
    _slaveaddr = int(_response["slaveaddr"])
    _startaddr = int(_response["startaddr"])
    _readquantity = int(_response["readquantity"])
    _ft03 = _response["ft03"]
    _ft02 = _response["ft02"]
    lora_tcp = _response["lora_tcp"]
    mqtt_tcp =  _response["mqtt_tcp"]
    enable_tcp = _response['enable_tcp']

    _active = True if enable_tcp else False

    _function_code = None
    if _ft03:
        _function_code = "03"
    elif _ft02:
        _function_code = "02"

    _result = {}
    _result['connected'] = 'True'

    modbus_tcp_dict = {"device":_device, "ip":_ip,"port":_port,"slave_id":_slaveaddr, "address":_startaddr,
                       "quantity":_readquantity, "function":_function_code, "timeout":5, "lora":lora_tcp, "mqtt":mqtt_tcp}

    conf.modbus_tcp_dict = modbus_tcp_dict

    modbus_tcp_list = conf.modbus_tcp_list
    modbus_tcp_list.append(modbus_tcp_dict)

    try:
        alter('config.py', "modbus_tcp = ", _active)
        alter('config.py',"modbus_tcp_dict = ", modbus_tcp_dict)
        alter('config.py', "modbus_tcp_list = ", modbus_tcp_list)
    except Exception as e:
        print(e)
        _result['connected'] = 'False'

    return Response(body=_result, headers={"Content-Type": "application/json"})

@app.route("/get/load/modbus", methods=["GET"])
def load_modbus(request):
    _tcp_dict = {}

    _tcp_dict['model'] = conf.modbus_tcp_dict
    _tcp_dict["data"] = conf.modbus_tcp_list

    _result = json.dumps(_tcp_dict)
    return Response(body=_result, headers={"Content-Type": "application/json"})

@app.route("/get/load/modbus_rtu", methods=["GET"])
def load_modbus_rtu(request):
    _tcp_dict = {}
    _tcp_dict["data"] = conf.modbus_rtu_list

    _result = json.dumps(_tcp_dict)
    return Response(body=_result, headers={"Content-Type": "application/json"})

@app.route("/post/delete/modbus", methods=["POST"])
def delete_modbus(request):
    _response = json.loads(request.body.decode())
    _id = int(_response["id"])
    modbus_tcp_list = conf.modbus_tcp_list
    modbus_tcp_list.pop(_id)
    alter('config.py', "modbus_tcp_list = ", modbus_tcp_list)

    return Response(body=None, headers={"Content-Type": "application/json"})

@app.route("/post/delete/modbus_rtu", methods=["POST"])
def delete_modbus(request):
    _response = json.loads(request.body.decode())
    _id = int(_response["id"])
    modbus_rtu_list = conf.modbus_rtu_list
    modbus_rtu_list.pop(_id)
    alter('config.py', "modbus_rtu_list = ", modbus_rtu_list)

    return Response(body=None, headers={"Content-Type": "application/json"})

@app.route("/post/save/modbus_rtu", methods=["POST"])
def save_modbus_rtu(request):
    _response = json.loads(request.body.decode())
    _baundrate = int(_response["baundrate"])

    _device = str(_response["device_rtu_no"])
    _slaveaddr = int(_response["rtu_slaveaddr"])
    _startaddr = int(_response["rtu_startaddr"])
    _readquantity = int(_response["rtu_readquantity"])
    _ft03 = _response["fr03"]
    _ft02 = _response["fr02"]

    lora_rtu = _response["lora_rtu"]
    mqtt_rtu =  _response["mqtt_rtu"]

    enable_rtu = _response['enable_rtu']

    _active = True if enable_rtu else False

    _function_code = None
    if _ft03:
        _function_code = "03"
    elif _ft02:
        _function_code = "02"

    _result = {}
    _result['connected'] = 'True'

    uart2_dict = {"tx": 17, "rx": 16, "baudrate": _baundrate, "data_bits": 8, "stop_bits": 1, "parity": None}

    modbus_rtu_dict = {"device": _device, "slave_id": _slaveaddr, "address": _startaddr,
                       "quantity": _readquantity, "function": _function_code, "timeout": 5, "lora":lora_rtu, "mqtt": mqtt_rtu}

    conf.modbus_rtu_dict = modbus_rtu_dict

    modbus_rtu_list = conf.modbus_rtu_list
    modbus_rtu_list.append(modbus_rtu_dict)

    try:
        alter('config.py', "uart2 = ", _active)
        alter('config.py',"uart2_dict = ", uart2_dict)
        alter('config.py', "modbus_rtu_list = ", modbus_rtu_list)
    except Exception as e:
        print(e)
        _result['connected'] = 'False'

    return Response(body=_result, headers={"Content-Type": "application/json"})

@app.route("/post/save/lora", methods=["POST"])
def save_lora(request):
    _response = json.loads(request.body.decode())

    _result = {}
    _result['connected'] = 'True'

    _fre = _response["frequency"]
    enable_lora = _response['enable_lora']

    _active = True if enable_lora else False

    try:
        alter('config.py',"lora_frequency = ", "{}".format(_fre))
        alter('config.py', "lora = ", _active)
    except Exception as e:
        print(e)
        _result['connected'] = 'False'

    return Response(body=_result, headers={"Content-Type": "application/json"})

@app.route("/post/save/receive_lora", methods=["POST"])
def save_receive_lora(request):
    _response = json.loads(request.body.decode())

    _result = {}
    _result['connected'] = 'True'

    _fre = int(_response["receive_frequency"])
    enable_lora = _response['enable_receive_lora']
    lora_receive_mqtt = _response['lora_receive_mqtt']
    lora_receive_uart = _response['lora_receive_uart']

    _active = True if enable_lora else False

    lora_receive_dict = {"frequency": _fre, "mqtt": lora_receive_mqtt, "uart2": lora_receive_uart}

    try:
        alter('config.py',"lora_receive_dict = ", lora_receive_dict)
        alter('config.py', "lora_receive_mode = ", _active)
    except Exception as e:
        print(e)
        _result['connected'] = 'False'

    return Response(body=_result, headers={"Content-Type": "application/json"})

@app.route("/post/save/mqtt", methods=["POST"])
def save_lora(request):
    _response = json.loads(request.body.decode())
    _result = {}
    _result['connected'] = 'True'

    _mqttip = _response["mqttip"]
    _mqttport = int(_response['mqttport']) if _response['mqttport'] != "" else 0
    _mqtttopic = _response['mqtttopic']
    _mqttuser = None if _response['mqttuser'] == "" else _response['mqttuser']
    _mqttpassword = None if _response['mqttpassword'] == "" else _response['mqttpassword']
    enable_mqtt = _response['enable_mqtt']

    _active = True if enable_mqtt else False

    mqtt_dict = {"topic":_mqtttopic.encode(), "last_will": b'dead', "broker_address": _mqttip,
                 "broker_port": _mqttport, "mqtt_user": _mqttuser, "mqtt_password": _mqttpassword}

    try:
        alter('config.py', "mqtt = ", _active)
        alter('config.py',"mqtt_dict = ",mqtt_dict)
    except Exception as e:
        print(e)
        _result['connected'] = 'False'

    return Response(body=_result, headers={"Content-Type": "application/json"})

@app.route("/get/load/heart", methods=["GET"])
def load_heart(request):

    _heart_dict = {}

    _heart_dict = conf.beat_heart_dict
    _result = json.dumps(_heart_dict)
    return Response(body=_result, headers={"Content-Type": "application/json"})

@app.route("/post/save/heart", methods=["POST"])
def save_heart(request):
    _response = json.loads(request.body.decode())
    _result = {}
    _result['connected'] = 'True'

    _heartip = _response["heartip"]
    _heartport = int(_response['heartport']) if _response['heartport'] != "" else 0
    _heartcontent = _response['heartcontent'] if _response['heartcontent'] != "" else '-B'
    _heartinterval = int(_response['heartinterval']) if _response['heartinterval'] != "" else 0

    enable_heart = _response['enable_heart']

    _active = True if enable_heart else False

    beat_heart_dict = {'heart_address': _heartip, 'heart_port': _heartport, 'heart_content': _heartcontent,
                       'interval': _heartinterval}

    try:
        alter('config.py', "beat_heart = ", _active)
        alter('config.py',"beat_heart_dict = ",beat_heart_dict)
    except Exception as e:
        print(e)
        _result['connected'] = 'False'

    return Response(body=_result, headers={"Content-Type": "application/json"})

#把config.py中的换位符从\r改为\n,因为在uPyCraft软件中，修改config后，会自动把\n修改为\r
#导致读取的时候不能自动换行
def replace_char(file):
    with open(file, mode='r', encoding='utf-8') as ff:
        f1 = ff.read()
        f2 = f1.replace('\r', '\n')

    with open(file, mode='w', encoding='utf-8') as f:
        f.write(f2)

#alter config.py file
def alter(file,key_str,value_str):
    #replace first
    replace_char(file)

    file_data = ""
    with open(file, "r", encoding="utf-8") as f:
        for line in f:
            if key_str in line:
                #line.partition(old_str) #return key_str
                line = key_str + str(value_str) +"\n"
            file_data += line

    with open(file, "w", encoding="utf-8") as f:
        f.write(file_data)

#initialize config.py
def init_config(file, file_init):
    file_data = ""
    with open(file_init, "r", encoding="utf-8") as f:
        for line in f:
            file_data += line

    with open(file, "w", encoding="utf-8") as f:
        f.write(file_data)
# app.run(debug=True)