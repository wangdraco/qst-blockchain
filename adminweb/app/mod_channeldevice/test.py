import time
from app.mod_redis.redis_class import Redis
_list = [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 23, 24, 0, 0, 0, 0, 0, 30]
print(_list[23:24])
print(time.strftime('%Y-%m-%d %H:%M:%S'))
# r = Redis.connect()
# print(r.keys('channel:145*'))
# if r.exists('channel:185:510'):
#     print('ddddddddddddddddddd=',r.get('channel:185:510'))
from pymodbus.client.sync import ModbusTcpClient, ModbusUdpClient, ModbusRtuFramer,ModbusSerialClient
# client = ModbusTcpClient('192.168.2.8', port='6003')
client = ModbusSerialClient(method='rtu', port='COM2',parity='O', baudrate=9600, timeout=1)

result = client.connect()
if result:
    _d = client.read_holding_registers(0,5,unit=1, signed=True)
    print(_d.registers)