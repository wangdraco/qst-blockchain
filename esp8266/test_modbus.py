from uModBus.tcp import TCP

_ip = '192.168.1.4'
modbus_obj = TCP(_ip)

slave_addr=0x01
starting_address=0x00
register_quantity=20
signed=True

register_value = modbus_obj.read_holding_registers(slave_addr, starting_address, register_quantity, signed)
print('Holding register value: ' + ' '.join('{:d}'.format(x) for x in register_value))




