from app.mod_protocalchannel.service import *
import app.mod_channelunit.service as cu_service
import app.mod_channeldevice.service as cd_service
from app.mod_redis.redis_class import Redis
from pymodbus.client.sync import ModbusTcpClient
import asyncio,threading,time,json
from decimal import Decimal
from app.mod_modbus import modbus_tools as mt

p_channels_list = select_by_clientAndIsactive(16,'Y')
channel_unit_list = cu_service.select_by_ClientAndIsactive(16,'Y')
channel_device_list = cd_service.select_by_ClientAndIsactive(16,'Y')

r = Redis.connect()

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


def process_holding_registers(channel,channel_unit,channel_devices,_result):
    #先过滤出channel_unit对应的channel_device
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



def process_channelunit(channel,channel_units,channel_devices,m_client):
    print('begin---------------')

    #开始遍历channel_unit，执行modbus操作
    for cu in channel_units:
        if cu.function_code == '03':
            try:
                result = m_client.read_holding_registers(cu.startfrom, cu.quantity,
                                                         unit=cu.unit_id, signed=True)
                print(f'{channel.channel_name}---{cu.device_name},process complete..........,result={result.registers}')
                process_holding_registers(channel,cu,channel_devices,result.registers)
            except Exception as e:
                #m_client.close()
                process_error_message(channel, None, cu, channel_devices)
                print(f'{channel.channel_name}---{cu.device_name},...读取错误...failure!!!!!!!!!!!',e)


def protocalchannel_threading(**name):
    channel = name['channel']
    channel_units = name['channel_unit']
    channel_devices = name['channel_device']

    try:
        client = ModbusTcpClient(channel.ipaddress, port=channel.port)
        result = client.connect()
        if result:#connected successful
            process_channelunit(channel,channel_units,channel_devices,client)
        else:
            #pass
            #连接错误，先看redis里有没有值，有的话找到后更新status=False，没有的话组装一个
            print(channel.channel_name, '--连接错误 failure-',name['channel_unit'])
            process_error_message(channel,channel_units,None,channel_devices)

    except Exception as e:
        print(channel.channel_name, '--failure----', e)


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

    try:
        t = threading.Thread(name=str(channel.id), target=protocalchannel_threading,
                             kwargs={'channel': channel,'channel_unit': _unit_list,'channel_device':_device_list})

        t.start()
    except Exception as e:
        print(t.name,'-thread error--',e)


async def main_task():
    for p in p_channels_list:
        await asyncio.gather(
            process_protocalchannels(p)
        )



# asyncio.run(main_task())

def schedule_run_task():

    while 1:
        asyncio.run(main_task())
        time.sleep(10)

schedule_run_task()