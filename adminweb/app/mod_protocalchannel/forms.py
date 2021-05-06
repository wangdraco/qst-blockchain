# coding: utf-8
from app import app,r
from flask_login import login_required
from flask import render_template,request,redirect,flash
from app.mod_protocalchannel.service import *
from app.mod_protocalchannel.models import protocalchannel
from app.mod_modbus.modbus_tools import calculateCRC
import json,struct,time
from pymodbus.client.sync import ModbusTcpClient,ModbusUdpClient, ModbusSerialClient,ModbusSocketFramer,ModbusRtuFramer



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

#根据channel_id，获取当前gprs通道的状态
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
        time.sleep(0.8)
        received = socket_client.recv(1024)
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

#下发modbus指令获取返回值，目前支持4G链接类型的modbus RTU设备
@app.route('/get/modbus/<int:channel_id>/<int:unit_id>,<int:code>,<int:start>,<int:quantity>')
def read_modbus(channel_id,unit_id,code,start,quantity):
    from app import client_socket
    result = {}
    channel = select_by_id(channel_id)
    if channel:
        if channel.connettype == 'gprs' or channel.connettype == 'gprs-l':#gprs，4G等链接从缓存中取client
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
        elif channel.connettype == 'tcp' or channel.connettype == 'tcp/ip' or channel.protocal_id == 1:#处理有线tcp或串口连接的方式
            client = None
            try:
                if channel.protocal_id == 1:  # 串口连接ModbusSerialClient(method='rtu', port='COM2', baudrate=9600,stopbits=1,parity='N'||'O'||'E',bytesize=8, timeout=1)
                    client = ModbusSerialClient(method='rtu', port=channel.port, stopbits=channel.stopbit,
                                                parity=channel.parity, baudrate=channel.baudrate,
                                                bytesize=channel.databit)
                elif channel.protocal_id == 2:  # modbus TCP/IP
                    client = ModbusTcpClient(channel.ipaddress, port=int(channel.port), framer=ModbusSocketFramer)
                elif channel.protocal_id == 3:  # modbus UDP
                    client = ModbusUdpClient(channel.ipaddress, port=int(channel.port), framer=ModbusSocketFramer)
                elif channel.protocal_id == 4:  # modbus TCP/IP over RTU
                    client = ModbusTcpClient(channel.ipaddress, port=int(channel.port), framer=ModbusRtuFramer)

                if code == 3: #READ_HOLDING_REGISTERS
                    _result = client.read_holding_registers(start, count=quantity, unit=unit_id, signed=True)
                    time.sleep(0.2)
                    # print('result is ', result)
                    result['data'] = _result.registers
                elif code == 2: #READ_DISCRETE_INPUTS
                    _result = client.read_discrete_inputs(start,quantity,unit=unit_id)
                    time.sleep(0.2)
                    result['data'] = result.bits
                elif code == 1:#READ_COILS
                    _result = client.read_coils(start, quantity, unit=unit_id)
                    time.sleep(0.2)
                    result['data'] = result.bits
                elif code == 4:#READ_INPUT_REGISTERS
                    _result = client.read_input_registers(start, count=quantity, unit=unit_id, signed=True)
                    time.sleep(0.2)
                    # print('result is ', result)
                    result['data'] = _result.registers

            except Exception as e:
                result['message'] = '连接设备出错了'
                print(e)

    else:
        result['message'] = '设备不存在'


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



