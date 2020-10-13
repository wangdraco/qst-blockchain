from app import app
from pymodbus.client.sync import ModbusTcpClient


@app.route('/post/<string:ip>/<int:port>/<int:unitid>/<int:regaddress>/<int:value>', methods=['POST'])
def process_write_registers(ip,port,unitid,regaddress,value):
    print('begin write coils=============================', ip, port)

    client = ModbusTcpClient(ip, port=port)

    result = client.write_register(regaddress, value, unit=unitid)
    print('result is ', result)

    client.close()


    return "succcess"




