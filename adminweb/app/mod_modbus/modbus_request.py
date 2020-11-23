from app import app
from pymodbus.client.sync import ModbusTcpClient


@app.route('/post/<string:ip>/<int:port>/<int:unitid>/<int:regaddress>/<int:value>', methods=['POST'])
def process_write_registers(ip,port,unitid,regaddress,value):
    print('begin write registers =============================', unitid, regaddress,value)

    r_result = 'false'

    try:
        client = ModbusTcpClient(ip, port=port)
        result = client.write_register(regaddress, value, unit=unitid)
        print('result is ', result)
        r_result = 'true'
    except Exception as e:
        r_result = 'false'
    finally:
        client.close()
    return r_result

@app.route('/get/<string:ip>/<int:port>/<int:unitid>/<int:regaddress>', methods=['GET'])
def process_read_registers(ip,port,unitid,regaddress):
    print('begin read registers =============================', unitid, regaddress)

    r_result = 0

    try:
        client = ModbusTcpClient(ip, port=port)
        result = client.read_holding_registers(regaddress, 1, unit=unitid, signed=True)
        #print('result is ', result)
        r_result = result.registers[0]
        print('result is ', r_result)
    except Exception as e:
        r_result = 'false'
    finally:
        client.close()
    return str(r_result)


