# coding: utf-8
from app import app,r
from flask_login import login_required
from flask import render_template,request,redirect,flash
from app.mod_protocalchannel.service import *
from app.mod_protocalchannel.models import protocalchannel
from app.mod_modbus.modbus_tools import calculateCRC
import json,struct,time



@app.route('/protocalchannel/list')
@login_required
def list_all_protocaldevice():
    _listdata = get_all_protocalchannels()
    return render_template("protocalchannel/protocalchannellist.html",listdata= _listdata)

@app.route('/protocalchannel/edit/<int:id>')
@login_required
def edit_protocalchannel(id):
    selectdata = protocalchannel()
    if (id != 0):
        selectdata = select_by_id(id)
    else:
        selectdata.id = 0
    return render_template("protocalchannel/protocalchannelform.html",selectdata= selectdata)


@app.route('/redis/<int:channel_id>/<int:channel_unit>')
def get_redis_data(channel_id,channel_unit):
    if r.exists(f'channel:{channel_id}:{channel_unit}'):
        return r.exists(f'channel:{channel_id}:{channel_unit}')
    else:
        result = {}
        result['result'] = False
        return json.dumps(result)

@app.route('/get/status/<int:channel_id>')
def get_channel_status(channel_id):
    message = ''
    status = False
    result = {}
    channel = select_by_id(channel_id)
    if channel:
        result['protocal'] = channel.protocal.protocal_name+channel.protocal.protocal_type
        result['address'] = channel.ipaddress
        result['port']= channel.port

        from app import client_socket
        for k, v in client_socket.items():
            if k == 'gprs-socket'+str(channel.port):
                message = '设备在线' if v['status'] else '设备离线了！'
                status = v['status']
                break
            else:
                message = '设备未启用'

    else:
        message = '没有此设备！'

    result['message'] = message
    result['status'] = status

    return json.dumps(result,ensure_ascii=False)

def process_modbus_read(socket_client,unit_id,code,start,quantity):
    # 组装_command，计算crc
    e = []
    real_temp = []
    for i in struct.pack('>BBHH', unit_id,code,start,quantity):  # unit,functioncode,start_address, read_num
        e.append(i)
    _command = calculateCRC(e, len(e), 0)
    while True:
        socket_client.sendall(bytes(_command))
        time.sleep(0.5)
        received = socket_client.recv(512)
        if received and len(received) > 5:
            print('received original data -----------------', received)
            temp = []  # convert to bytes array

            for j in received:
                temp.append(j)
            # 确保返回的数据是正确的modbus顺序 [unitid,functionCode,readNumber,......]
            if temp.index(_command[1]) - temp.index(_command[0]) == 1:  # unitid 和functioncode紧挨着
                print('command[1]=',_command[1],' and _command[0]=',_command[0])
                real_temp = temp[temp.index(_command[2]):]

            print('send command is =================', _command)
            print(f' received real data is {temp}, {real_temp}')

            break
    return real_temp

def get_connect_fromport(port):
    from app import client_socket
    client = None
    _sock = client_socket['gprs-socket' + str(port)]

    if _sock and _sock['status']:
        # print('get socket from app.client_socket-------------------------','gprs-socket' + str(channel.port))
        client = _sock['sock']

    return client

@app.route('/get/modbus/<int:channel_id>/<int:unit_id>,<int:code>,<int:start>,<int:quantity>')
def read_modbus(channel_id,unit_id,code,start,quantity):
    from app import client_socket
    result = {}
    channel = select_by_id(channel_id)
    if channel:
        _status = get_channel_status(channel_id)
        status = json.loads(_status)

        result['protocal'] = channel.protocal.protocal_name + channel.protocal.protocal_type
        result['address'] = channel.ipaddress
        result['port'] = channel.port

        _sock = client_socket['gprs-socket' + str(channel.port)]
        if status['status']:
            try:
                _socket = _sock['sock']
                _socket.settimeout(3)
                _result = process_modbus_read(_socket, unit_id, code, start, quantity)
                result['data'] = _result
            except Exception as e:
                result['message'] = '读取设备出错了'
        else:
            result['message'] = '设备不在线'

    else:
        result['message'] = '设备存在'


    return json.dumps(result,ensure_ascii=False)

@app.route('/get/<int:port>/config')
def get_port_config(port):
    _sock = get_connect_fromport(str(port))
    result = {}
    _command = {}
    _command['Function'] = 'ConfigInquire'
    _sock.sendall(bytes(json.dumps(_command),encoding='utf-8'))
    time.sleep(0.7)
    received = _sock.recv(1024)
    if len(received)>5:
        result = json.loads(received,encoding='utf-8')
    print('received============================================',received)
    return json.dumps(result)



