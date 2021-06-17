import struct,asyncio,json,datetime

from app.mod_modbus.water_electronic_devices import device_list

# r =  Redis.connect()

def generate_redis_data(_device,_value):
    _data = {"data":[{"client_id":_device["client_id"],"equipmentTableName":_device["equipmentTableName"],"id":1,"equipment_id":_device["equipment_id"],
                      "equipmentName":_device["equipmentName"],"community_status":"true","startstop_status":"true",
                      "update_time":datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M:%S"),"current_value":_value}]}
    redis_data = json.dumps(_data)
    # r.publish('wsdata', str(redis_data))

#just for modbus CRC
def calculateCRC(data, numberOfBytes, startByte):
    crc = 0xFFFF
    crc_result = []
    for x in range(0, numberOfBytes):
        crc = crc ^ data[x]
        for _ in range(0, 8):
            if ((crc & 0x0001) != 0):
                crc = crc >> 1
                crc = crc ^ 0xA001
            else:
                crc = crc >> 1
    #crc_result.append(crc&0xFF)
    #crc_result.append((crc&0xFF00) >> 8)
    data.append(crc & 0xFF)
    data.append((crc&0xFF00) >> 8)

    '''return crc'''
    return data

#convert int to bytes ,so we can send them via socket
def int2bytes(int_data):
    temp = []
    #for regular modbus ,like read_holding_register ,unit(1byte)+function_code(1byte)+address(2bytes)+readNumbers(2bytes)
    # use int.to_bytes() method
    temp.append((int_data[0]).to_bytes(1, byteorder='big')[0])
    temp.append((int_data[1]).to_bytes(1, byteorder='big')[0])
    temp.append((int_data[2]).to_bytes(2, byteorder='big')[0])
    temp.append((int_data[2]).to_bytes(2, byteorder='big')[1])
    temp.append((int_data[3]).to_bytes(2, byteorder='big')[0])
    temp.append((int_data[3]).to_bytes(2, byteorder='big')[1])
    return temp


#modbus slave --- Float AB CD
#'%04x' 是格式化操作，表示把%右边的变量格式化为带有四位数的十六进制数（没有0x开头），位数不够的时候，左侧填充0,比hex()方法灵活
#高位在后的顺序转成浮点数(ABCD),如果reverse=True,则是CDAB
#usage: ReadFloat((0,2400),reverse=False)
def ReadFloat(*args,reverse=False):
    for m ,n in args:
        m, n = '%04x' % m, '%04x' % n
    if reverse:
        v = n + m
    else:
        v = m + n
    print(v)
    y_bytes = bytes.fromhex(v)
    y = struct.unpack('!f',y_bytes)[0]
    y = round(y,2)
    return y

def WriteFloat(value,reverse=False):
    y_bytes = struct.pack('!f',value)
    # y_hex = bytes.hex(y_bytes)
    y_hex = ''.join(['%02x' % i for i in y_bytes])
    m, n = y_hex[:-4],y_hex[-4:]
    m, n = int(m,16),int(n,16)
    if reverse:
        v = [n,m]
    else:
        v = [m,n]
    return v

#modbus slave --- Long AB CD
def ReadLongInt(*args,reverse=False):
    for m, n in args:
        m, n = '%04x' % m, '%04x' % n
    if reverse:
        v = n + m
    else:
        v = m + n
    y_bytes = bytes.fromhex(v)
    y = struct.unpack('!i',y_bytes)[0]
    return y

def WriteLongInt(value,reverse=False):
    y_bytes = struct.pack('!i',value)
    # y_hex = bytes.hex(y_bytes)
    y_hex = ''.join(['%02x' % i for i in y_bytes])
    m, n = y_hex[:-4],y_hex[-4:]
    m, n = int(m,16),int(n,16)
    if reverse:
        v = [n,m]
    else:
        v = [m,n]
    return v


#有些modbus设备得到的数据是负数，比如温度，一般是以补码形式上传，
#比如modbus读到一条温度数据是 65435, 或者0xFF9B，实际应该是-101
def get_negative(original):
    # 补码取反，再加1，得到负数的原码，0xFFFF表示是对16位数而言
    return 0 - ((original ^ 0xFFFF) + 1)  # original=65435，得到101,再取负

def get_positive(original):
    # 与运算，得到负数的补码，0xFFFF表示是对16位数而言
    return original & 0xFFFF  # original = -101,得到 65435

from pymodbus.client.sync import ModbusTcpClient,ModbusRtuFramer


#normal tcp


def read_modbus_tcp(_point):
    final_result = 0
    client = ModbusTcpClient(_point["ip"], port=_point["port"])

    result = client.read_holding_registers(_point["begin"], _point["length"], unit=_point["unit_id"], signed=True)

    print(f'{_point["building_no"]}--{_point["device_name"]} result is {result.registers}')

    if _point["formate"] == "ABCD":
        final_result = ReadLongInt((result.registers[0],result.registers[1]))
    elif _point["formate"] == "CDAB":
        final_result = ReadLongInt((result.registers[0], result.registers[1]),reverse=True)

    client.close()

    #call redis publish
    generate_redis_data(_point,final_result)
    print("final result is",final_result)



async def modbus_read_task(_point, time_ms):
    while True:
        try:
            read_modbus_tcp(_point)
        except Exception as e:
            print(f'{_point["building_no"]}--{_point["device_name"]}  error-------------------',e)
        await asyncio.sleep(time_ms)


async def main(duration):
    _devices = device_list["devices"]
    #loop = asyncio.get_event_loop()
    for p in _devices:
        await asyncio.sleep(2) #加上这个，可以让不同的任务之间有5秒的间隔
        asyncio.create_task(modbus_read_task(p,duration))
    while True:
        await asyncio.sleep(1)

    #loop.run_forever()


def run(duration=10):
    try:
        asyncio.run(main(duration))
    except Exception as e:
        print('Interrupted',e)
    finally:
        asyncio.new_event_loop()
        print('asyncio run again.')

if __name__ == "__main__":
    # run()
    print('after asyncio')
