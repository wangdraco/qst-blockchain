# -*- coding: UTF8 -*-
import uasyncio as asyncio
import usocket as socket,machine
import config as conf

from umqtt.simple import MQTTClient

client_id = conf.mac_id



def mqtt_pub(_payload):
    broker_address = conf.broker_address
    broker_port = conf.broker_port
    topic = conf.topic
    client = MQTTClient(client_id, broker_address,port=broker_port)
    client.set_last_will(topic, conf.last_will)
    client.connect()
    client.publish(topic, str(client_id+','+_payload),qos=1)
    print('send MQTT ')
    client.disconnect()

def beat_heart():

    sock = socket.socket()
    sock.connect((conf.heart_address, conf.heart_port))
    sock.send((conf.heart_content).encode('utf-8'))  # data+'\n'
    print('send beat ',conf.heart_content)
    sock.close()

def uart():
    uart = None
    if conf.uart1:
        uart = machine.UART(1, baudrate=conf.uart1_dict["baudrate"], tx=conf.uart1_dict["tx"],
                        rx=conf.uart1_dict["rx"], bits=conf.uart1_dict["data_bits"], parity=conf.uart1_dict["parity"], stop=conf.uart1_dict["stop_bits"]) #pin 25,26
    if conf.uart2:
        uart = machine.UART(2, baudrate=conf.uart2_dict["baudrate"], tx=conf.uart2_dict["tx"],
                            rx=conf.uart2_dict["rx"], bits=conf.uart2_dict["data_bits"], parity=conf.uart2_dict["parity"],
                            stop=conf.uart2_dict["stop_bits"])  # pin 16,17
    #uart.read()
    return uart

def modbus_serial():
    from serial import Serial
    modbus_obj = None

    try:
        if conf.uart1:
            modbus_obj = Serial(1, baudrate=conf.uart1_dict["baudrate"], tx=conf.uart1_dict["tx"],
                                rx=conf.uart1_dict["rx"],
                                data_bits=conf.uart1_dict["data_bits"], stop_bits=conf.uart1_dict["stop_bits"],
                                parity=conf.uart1_dict["parity"])

        if conf.uart2:
            modbus_obj = Serial(2, baudrate=conf.uart2_dict["baudrate"], tx=conf.uart2_dict["tx"],
                                rx=conf.uart2_dict["rx"],
                                data_bits=conf.uart2_dict["data_bits"], stop_bits=conf.uart2_dict["stop_bits"],
                                parity=conf.uart2_dict["parity"])
    except Exception as e:
        pass
    return modbus_obj

def modbus_tcp():
    from tcp import TCP
    modbus_obj = None
    try:
        modbus_obj = TCP(conf.modbus_tcp_dict["ip"], slave_port=conf.modbus_tcp_dict["port"])
    except Exception as e:
        pass
    return modbus_obj

def uart_modbus_read(modbus_obj):
    slave_addr = 0x01
    starting_address = 0x00
    register_quantity = 2
    signed = True

    register_value = modbus_obj.read_holding_registers(slave_addr, starting_address, register_quantity, signed)
    print('Holding register value: ',register_value)
    mqtt_pub('test-data'+str(register_value[0])+","+str(register_value[1]))

def tcp_modbus_read(modbus_obj):
    slave_addr = 0x01
    starting_address = 0x00
    register_quantity = 10
    signed = True

    register_value = modbus_obj.read_holding_registers(slave_addr, starting_address, register_quantity, signed)
    print('Holding register value: ' + ' '.join('{:d}'.format(x) for x in register_value))


class WiFi:

    def __init__(self, ssid = conf.SSID, password = conf.PASSWORD):
        self.SSID = ssid
        self.PASSWORD = password

    def connect(self):
        import network

        sta = network.WLAN(network.STA_IF)
        # ap_if = network.WLAN(network.AP_IF)
        # ap_if.active(conf.ap_mode)
        # ap_if.config(essid=conf.ap_essid, channel=11,authmode=network.AUTH_WPA_WPA2_PSK, password=conf.ap_password)
        if not sta.isconnected():
            try:
                sta.active(True)
                sta.scan()
                sta.connect(self.SSID, self.PASSWORD)
            except Exception as e:
                print('wifi connect error !!!!', e)
            else:
                print('begin wifi connecting...,')
        return sta

    def ap(self):# 暂时不用,ap功能直接放到boot方法里，自动启动
        import network
        ap_if = network.WLAN(network.AP_IF)
        ap_if.active(conf.ap_mode)
        ap_if.config(essid=conf.ap_essid, channel=11, password=conf.ap_password)
        print('ap status is ',ap_if.status())

    async def wifi_connect_task(self,_point, time_ms):# 暂时不用，路由器重启后，其他程序会自动连接的
        import network
        sta = network.WLAN(network.STA_IF)

        while not sta.isconnected():
            try:
                sta.active(True)
                sta.scan()
                sta.connect(self.SSID, self.PASSWORD)
            except Exception as e:
                print('wifi connect error !!!!', e)
            else:
                print('connected,',sta.status())
            await asyncio.sleep(time_ms)

class Multitask():
    def __init__(self,_sleep = 10):
        self.sleep = _sleep

    async def gc_collect(self):
        import gc
        while True:
            try:
                gc.collect()
            except Exception as e:
                print('gc error',e)
            await asyncio.sleep(self.sleep)  # Pause 4s

    async def mqtt(self):
        while True:
            try:
                #print('sent mqtt msg')
                mqtt_pub('test-data')
            except Exception as e:
                print('mqtt  error', e)
            await asyncio.sleep(self.sleep)  # Pause 4s


    async def beat(self):
        while True:
            #sock = socket.socket()
            try:
                beat_heart()
            except Exception as e:
                print('beat heart socket error', e)
            await asyncio.sleep(self.sleep)  # Pause 4s

    async def uart_send(self):
        modbus_obj = modbus_serial()
        while True:
            #sock = socket.socket()
            try:
                uart_modbus_read(modbus_obj)
            except Exception as e:
                print('uart send error', e)
                await asyncio.sleep(5)
                modbus_obj = modbus_serial()
            await asyncio.sleep(self.sleep)  # Pause 4s

    async def modbustcp_send(self):
        modbus_obj = modbus_tcp()
        while True:
            try:
                uart_modbus_read(modbus_obj)
            except Exception as e:
                print('modbus tcp send error', e)
                await asyncio.sleep(5)
                modbus_obj = modbus_tcp()

            await asyncio.sleep(self.sleep)  # Pause 4s

    async def food(self,p4):
        while True:
            p4.value(1)
            print('value +++++ ', p4.value())
            await asyncio.sleep_ms(self.sleep)
            p4.value(0)
            print('value ==== ', p4.value())
            await asyncio.sleep_ms(self.sleep)


def run_multi_task():
    _task = Multitask()
    loop = asyncio.get_event_loop()
    loop.call_soon(_task.beat(), 3)
    loop.call_later(2, _task.mqtt(), 5)
    # loop.create_task(test.beat()) # Schedule ASAP
    loop.run_forever()








