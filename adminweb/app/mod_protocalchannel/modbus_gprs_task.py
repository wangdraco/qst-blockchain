# coding: utf-8

from app.mod_protocalchannel.service import *
import app.mod_channelunit.service as cu_service
import app.mod_channeldevice.service as cd_service
from app.mod_redis.redis_class import Redis
import asyncio,threading,time,json,socket,struct
from decimal import Decimal
from app.mod_modbus import modbus_tools as mt

from app import client_socket,client_id
from app.mod_modbus.modbus_tools import  calculateCRC

p_channels_list =[]
channel_unit_list =[]
channel_device_list = []
try:
    p_channels_list = select_by_clientAndIsactive(client_id, 'Y')
    # p_channels_list = select_by_ids([1])
    channel_unit_list = cu_service.select_by_ClientAndIsactive(client_id, 'Y')
    channel_device_list = cd_service.select_by_ClientAndIsactive(client_id, 'Y')
except Exception as e:
    print("出错了0000000000",e)


print('-------------------',channel_unit_list)

from app import r
# r = Redis.connect()

def process_error_message(channel=None,channel_unit_list=None,channel_unit=None,channel_devices=None):
    if channel and channel_unit_list:#连接错误

        for cu in channel_unit_list:
            _devices = []
            for cd in channel_devices:
                if cd.channelunit_id == cu.id:
                    _devices.append(cd.toDict())

            if r.exists(f'channel:{channel.id}:{cu.id}'):#redis里已经存在过完整的数据，则把status设置为false
                _result = json.loads(r.get(f'channel:{channel.id}:{cu.id}'))
                _result['status'] = False
                _result = json.dumps(_result,ensure_ascii=False)
                Redis.set_data(r, f'channel:{channel.id}:{cu.id}', _result)
            else: #在redis里没有对应的数据，则生成一个默认的
                _data = {'channel_id': channel.id, "channel_name": channel.channel_name, 'ip': channel.ipaddress,
                         'port': channel.port, 'status': False, 'record_time': time.strftime('%Y-%m-%d %H:%M:%S'),
                         'channel_unit': {'channelunit_id': cu.id, 'device_name': cu.device_name,
                                          'unit_id': cu.unit_id, 'func_code': cu.function_code,
                                          'startfrom': cu.startfrom, 'quantity': cu.quantity,
                                          'status': False, 'devices': _devices}}
                redis_data = json.dumps(_data, ensure_ascii=False)
                Redis.set_data(r, f'channel:{channel.id}:{cu.id}', redis_data)

    elif channel and channel_unit:#读取错误
        if r.exists(f'channel:{channel.id}:{channel_unit.id}'):  # redis里已经存在过完整的数据，则把status设置为false
            _result = json.loads(r.get(f'channel:{channel.id}:{channel_unit.id}'))
            _result['status'] = True  #连接正常
            _result['channel_unit']['status'] = False  #读取失败
            _result = json.dumps(_result, ensure_ascii=False)
            Redis.set_data(r, f'channel:{channel.id}:{channel_unit.id}', _result)
        else:  # 在redis里没有对应的数据，则生成一个默认的
            _devices = []
            for cd in channel_devices:
                if cd.channelunit_id == channel_unit.id:
                    _devices.append(cd.toDict())
            _data = {'channel_id': channel.id, "channel_name": channel.channel_name, 'ip': channel.ipaddress,
                     'port': channel.port, 'status': True, 'record_time': time.strftime('%Y-%m-%d %H:%M:%S'),
                     'channel_unit': {'channelunit_id': channel_unit.id, 'device_name': channel_unit.device_name,
                                      'unit_id': channel_unit.unit_id, 'func_code': channel_unit.function_code,
                                      'startfrom': channel_unit.startfrom, 'quantity': channel_unit.quantity,
                                      'status': False, 'devices': _devices}}
            redis_data = json.dumps(_data, ensure_ascii=False)
            Redis.set_data(r, f'channel:{channel.id}:{channel_unit.id}', redis_data)


def process_modbus_results(channel,channel_unit,channel_devices,_result):
    #先过滤出channel_unit对应的channel_device
    print('最终要处理的result======',_result)
    _devices = []
    for cd in channel_devices:
        if cd.channelunit_id == channel_unit.id:
            _devices.append(cd)

    result_list = []
    for cd in _devices:
        if cd.quantity == 1:
            cd.original_result = _result[cd.startfrom:cd.startfrom+cd.quantity][0]
            if cd.istransfer in ('Y',"true"):
                cd.final_result = str(Decimal(str(cd.original_result)) * Decimal(str(cd.offset)))
            else:
                cd.final_result = cd.original_result
        elif cd.quantity == 2:
            _first = _result[cd.startfrom:cd.startfrom + cd.quantity][0]
            _second = _result[cd.startfrom:cd.startfrom + cd.quantity][1]
            _tuple = (_first, _second)
            _r = 0
            if cd.data_type == 'int':
                _r = mt.ReadLongInt(_tuple, reverse = True if cd.data_order == 'CDAB' else False)
            elif cd.data_type == 'float':
                _r = mt.ReadFloat(_tuple, reverse=True if cd.data_order == 'CDAB' else False)
            cd.original_result = _r
            if cd.istransfer in ('Y',"true"):
                cd.final_result = str(Decimal(str(_r)) * Decimal(str(cd.offset)))
            else:
                cd.final_result = _r

        result_list.append(cd.toDict())

    _data = {'channel_id':channel.id, "channel_name":channel.channel_name, 'ip':channel.ipaddress,
             'port':channel.port,'status':True,'record_time':time.strftime('%Y-%m-%d %H:%M:%S'),
             'channel_unit':{'channelunit_id':channel_unit.id,'device_name':channel_unit.device_name,
                             'unit_id':channel_unit.unit_id,'func_code':channel_unit.function_code,
                             'startfrom':channel_unit.startfrom,'quantity':channel_unit.quantity,
                             'status':True,'devices':result_list}}
    #把结果放到redis中，key=channel:channel.id:channel_unit.id
    redis_data = json.dumps(_data,ensure_ascii=False)
    Redis.set_data(r,f'channel:{channel.id}:{channel_unit.id}',redis_data)

    print(f'the device is =={channel_unit.device_name}===key is channel:{channel.id}:{channel_unit.id}====={redis_data}')

def process_modbus_read(channelunit,socket_client):
    # 组装_command，计算crc
    e = []
    real_temp = []
    for i in struct.pack('>BBHH', channelunit.unit_id, function_code_to_num(channelunit.function_code),
                         channelunit.startfrom,channelunit.quantity):  # unit,functioncode,start_address, read_num
        e.append(i)
    _command = calculateCRC(e, len(e), 0)
    while True:
        socket_client.sendall(bytes(_command))
        time.sleep(0.5)
        received = socket_client.recv(1024)
        if received and len(received) > 5:
            print('received original data -----------------', received)
            temp = []  # convert to bytes array

            for j in received:
                temp.append(j)
            # 确保返回的数据是正确的modbus顺序 [unitid,functionCode,readNumber,......]
            if temp[0]==_command[0] and temp[1]==_command[1]:  # unitid 和functioncode紧挨着
                real_temp = temp[3:] #前三位分别是unitid，funcode，读取数量

            print('send command is =================', _command)
            print(f' received real data is {temp}, {real_temp}')

            break
    return real_temp

def process_channelunit(channel,channel_units,channel_devices,m_client):


    #开始遍历channel_unit，执行modbus操作
    for cu in channel_units:
        print('begin---------channelunit------',cu)

        try:
            if cu.function_code == '03' or cu.function_code == 'READ_HOLDING_REGISTERS':

                result = process_modbus_read(cu,m_client)
                print(f'{channel.channel_name}---{cu.device_name},process complete..........,result={result}')
                #result 里是bytes数组[0,25,0,32,0,....],8位一个，要整理成16位一组的
                _result = []
                for i in range(0, int(len(result) / 2)):
                    i = i * 2
                    _result.append(struct.unpack('>H', bytes([result[i], result[i + 1]]))[0])

                process_modbus_results(channel, cu, channel_devices, _result)

            elif cu.function_code == '02' or cu.function_code == 'READ_DISCRETE_INPUTS':
                pass
            elif cu.function_code == '01' or cu.function_code == 'READ_COILS':
                pass
            elif cu.function_code == '04' or cu.function_code == 'READ_INPUT_REGISTERS':
                pass

        except Exception as e:
            # m_client.close()
            process_error_message(channel, None, cu, channel_devices)
            print(f'{channel.channel_name}---{cu.device_name},...读取错误...failure!!!!!!!!!!!', e)
        time.sleep(1)
    # if m_client:
    #     m_client.close()





def get_connect(channel):
    client = None
    _sock = client_socket['gprs-socket' + str(channel.port)]
    print('in get_connect is 9999999999999999999999999',_sock)
    if _sock and _sock['status']:
        print('get socket from app.client_socket-------------------------','gprs-socket' + str(channel.port))
        client = _sock['sock']

    return client


def protocalchannel_threading(**name):
    channel = name['channel']
    channel_units = name['channel_unit']
    channel_devices = name['channel_device']

    try:
        client = get_connect(channel)
        if client:#connected successful
            client.settimeout(3) #设置读写超时为3秒
            process_channelunit(channel,channel_units,channel_devices,client)
        else:
            #pass
            #连接错误，先看redis里有没有值，有的话找到后更新status=False，没有的话组装一个
            print(channel.channel_name, '--socket链路未连接或连接错误 failure-',name['channel_unit'])
            process_error_message(channel,channel_units,None,channel_devices)

    except Exception as e:
        print(channel.channel_name, '--超时或处理出错了----', e)


async def process_protocalchannels(channel):

    #整理数据，一个通道下面多个channelunit，一个channelunit多个channeldevice
    _unit_list = []
    _device_list = []
    # filter channelunit by protocalchannel_Id
    for channel_unit in channel_unit_list:
        if channel_unit.protocalchannel_id == channel.id and channel_unit.isactive == 'Y':
            _unit_list.append(channel_unit)

            # filter channeldevice by channelunit_Id
            for d in channel_device_list:
                if d.channelunit_id == channel_unit.id:
                    _device_list.append(d)
    #如果有channelunit和channeldevice，则启动线程进行读取操作
    if len(_unit_list)>0 and len(_device_list)>0:
        try:
            t = threading.Thread(name=str(channel.id), target=protocalchannel_threading,
                                 kwargs={'channel': channel, 'channel_unit': _unit_list,
                                         'channel_device': _device_list})

            t.start()
            #time.sleep(0.2)
        except Exception as e:
            print(t.name, '-thread error--', e)



#function code to number
def function_code_to_num(fc_code):
    default_fccode = 3
    if 'READ_HOLDING_REGISTERS' == fc_code or '03' == fc_code:
        default_fccode = 3
    elif 'READ_COILS' == fc_code or '01'== fc_code:
        default_fccode = 1
    elif 'READ_INPUT_DISCRETES' == fc_code or '02'== fc_code:
        default_fccode = 2
    elif 'READ_INPUT_REGISTERS' == fc_code or '04'== fc_code:
        default_fccode = 4
    elif 'WRITE_COIL' == fc_code or '05'== fc_code:
        default_fccode = 5
    elif 'WRITE_SINGLE_REGISTER' == fc_code or '06'== fc_code:
        default_fccode = 6

    return default_fccode

async def main_gprs_task():
    for p in p_channels_list:
        if p.connettype == 'gprs' or p.connettype == 'gprs-l': # 把gprs，4G设备单独处理，涉及到透传
            #
            await asyncio.gather(process_protocalchannels(p))


def schedule_gprs_task():
    # socket_thread()
    print('---------------------------------')
    while 1:
        time.sleep(126)  # m每隔126秒执行一下modbus读取命令 ,等gprs设备第一次连接以后再执行
        asyncio.run(main_gprs_task())




if __name__ == "__main__":
    schedule_gprs_task()
