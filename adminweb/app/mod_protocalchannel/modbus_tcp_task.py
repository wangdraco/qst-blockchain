# coding: utf-8

from app.mod_protocalchannel.service import *
import app.mod_channelunit.service as cu_service
import app.mod_channeldevice.service as cd_service
from app.mod_redis.redis_class import Redis
from pymodbus.client.sync import ModbusTcpClient,ModbusUdpClient, ModbusSerialClient,ModbusSocketFramer,ModbusRtuFramer
import asyncio,threading,time,json
from decimal import Decimal
from app.mod_modbus import modbus_tools as mt
from app import client_id
from apscheduler.schedulers.blocking import BlockingScheduler



scheduler = BlockingScheduler()


p_channels_list = select_by_clientAndIsactive(client_id,'Y')
# p_channels_list = select_by_ids([1])
channel_unit_list = cu_service.select_by_ClientAndIsactive(client_id,'Y')
channel_device_list = cd_service.select_by_ClientAndIsactive(client_id,'Y')

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


def process_modbus_results(channel,channel_unit,channel_devices,_result):
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

    #开始遍历channel_unit，执行modbus操作
    for cu in channel_units:
        try:
            if cu.function_code == '03' or cu.function_code == 'READ_HOLDING_REGISTERS':
                result = m_client.read_holding_registers(cu.startfrom, cu.quantity,
                                                         unit=cu.unit_id, signed=True)
                print(f'{channel.channel_name}---{cu.device_name},process complete..........,result={result.registers}')
                process_modbus_results(channel, cu, channel_devices, result.registers)
            elif cu.function_code == '02' or cu.function_code == 'READ_DISCRETE_INPUTS':
                result = m_client.read_discrete_inputs(cu.startfrom,cu.quantity,unit=cu.unit_id)
                process_modbus_results(channel, cu, channel_devices, result.bits)
            elif cu.function_code == '01' or cu.function_code == 'READ_COILS':
                result = m_client.read_coils(cu.startfrom,cu.quantity,unit=cu.unit_id)
                process_modbus_results(channel, cu, channel_devices, result.bits)
            elif cu.function_code == '04' or cu.function_code == 'READ_INPUT_REGISTERS':
                result = m_client.read_input_registers(cu.startfrom,cu.quantity,unit=cu.unit_id)
                process_modbus_results(channel, cu, channel_devices, result.registers)

        except Exception as e:
            # m_client.close()
            process_error_message(channel, None, cu, channel_devices)
            print(f'{channel.channel_name}---{cu.device_name},...读取错误...failure!!!!!!!!!!!', e)

def get_connect(channel):
    client = None
    try:
        if channel.protocal_id == 1:  # 串口连接ModbusSerialClient(method='rtu', port='COM2', baudrate=9600,stopbits=1,parity='N'||'O'||'E',bytesize=8, timeout=1)
            client = ModbusSerialClient(method='rtu',port=channel.port,stopbits=channel.stopbit,
                                        parity=channel.parity,baudrate=channel.baudrate,
                                        bytesize=channel.databit)
        elif channel.protocal_id == 2:  # modbus TCP/IP
            client = ModbusTcpClient(channel.ipaddress, port=int(channel.port), framer=ModbusSocketFramer)
        elif channel.protocal_id == 3: #modbus UDP
            client = ModbusUdpClient(channel.ipaddress, port=int(channel.port), framer=ModbusSocketFramer)
        elif channel.protocal_id == 4:  # modbus TCP/IP over RTU
            client = ModbusTcpClient(channel.ipaddress, port=int(channel.port), framer=ModbusRtuFramer)

    except Exception as e:
        print('get connect 出错了.',e)

    return client


def protocalchannel_threading(**name):
    channel = name['channel']
    channel_units = name['channel_unit']
    channel_devices = name['channel_device']

    try:
        client = get_connect(channel)

        if client and client.connect():#connected successful
            process_channelunit(channel,channel_units,channel_devices,client)

            #用完就关闭连接，如果不关闭，串口连接的时候会出问题，但tcp没问题
            client.close()
        else:
            #pass
            #连接错误，先看redis里有没有值，有的话找到后更新status=False，没有的话组装一个
            print(channel.channel_name, '--连接错误 failure-',name['channel_unit'],' client is ',client.__dict__,' status=',client.connect())
            process_error_message(channel,channel_units,None,channel_devices)

    except Exception as e:
        print(channel.channel_name, '--failure----', e)

def schedule_jobs(**name):
    channel = name['channel']
    _unit_list = name['channel_unit']
    _device_list = name['channel_device']

    t = threading.Thread(name=str(channel.id), target=protocalchannel_threading,
                         kwargs={'channel': channel, 'channel_unit': _unit_list,
                                 'channel_device': _device_list})

    t.start()

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

    if len(_unit_list) > 0:
        try:
            # t = threading.Thread(name=str(channel.id), target=protocalchannel_threading,
            #                      kwargs={'channel': channel, 'channel_unit': _unit_list,
            #                              'channel_device': _device_list})
            #
            # t.start()

            scheduler.add_job(schedule_jobs,
                              'interval',
                              kwargs={'channel': channel,
                                      'channel_unit': _unit_list,
                                      'channel_device': _device_list},
                              seconds=channel.refreshtime)
        except Exception as e:
            print(scheduler, '-启动定时任务的时候出错了--', e)


async def main_tcpip_task():
    for p in p_channels_list:
        if p.connettype == 'tcp' or p.connettype == 'tcp/ip' or p.protocal_id == 1:  # 只处理有线tcp或串口连接的方式
            await asyncio.gather(
                process_protocalchannels(p)
            )
    await asyncio.sleep(1)# 如果没有这行，则APScheduler的job不启动，就是等上面的gather完成了
    scheduler.start()


def schedule_tcpip_task():
    # while 1:
    #     time.sleep(10)
    #     asyncio.run(main_tcpip_task())
    #使用APScheduler执行定期任务（根据每个通道的refreshtime），否则就使用上面的代码定期执行
    asyncio.run(main_tcpip_task())


if __name__ == "__main__":
    schedule_tcpip_task()
