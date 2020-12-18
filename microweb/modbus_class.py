# -*- coding: UTF8 -*-

class modbus:

    def __init__(self,slave_addr,starting_address,register_quantity,signed=True):

        self.modbus_obj = None
        self.slave_addr = slave_addr
        self.starting_address = starting_address
        self.register_quantity = register_quantity
        self.signed = signed

    def read_holding_registers(self):
        register_value = self.modbus_obj.read_holding_registers(self.slave_addr, self.starting_address, self.register_quantity, self.signed)

        return register_value
    def read_discrete_inputs(self):

        discrete_value = self.modbus_obj.read_discrete_inputs(self.slave_addr, self.starting_address,self.register_quantity)
        return discrete_value


    def modbus_serial(self,_baudrate):
        from serial import Serial
        self.modbus_obj = None
        try:
            self.modbus_obj = Serial(2, baudrate=_baudrate, tx=17,rx=16,
                                data_bits=8, stop_bits=1,parity=None)
        except Exception as e:
            pass
        return self.modbus_obj

    def modbus_tcp(self,_ip,_port):
        from uModBus.tcp import TCP
        self.modbus_obj = None
        try:
            self.modbus_obj = TCP(_ip, slave_port=_port)
        except Exception as e:
            pass
        return self.modbus_obj

if __name__ == "__main__":
    try:
        m = modbus(1, 0, 10)
        m.modbus_tcp('192.168.2.4', 6001)
        print(m.read_holding_registers())
    except Exception as e:
        print(e)





