# -*- coding: UTF8 -*-
# Micropython global config files
# Author: Draco.Wang <1599980410@qq.com>
# import ubinascii,machine
# mac_id = str(ubinascii.hexlify(machine.unique_id()),'utf-8')
mac_id = 'localtest222'

#gc collect
gc_collect = True

#web username&password
web_username = 'admin'
web_password = '1234'

sta_mode = False
SSID = 'tw-gelou222'
PASSWORD = 'netgear168'

ap_mode = True
ap_essid = "lora-"+mac_id
ap_password = "yunwei168"

#mqtt config
mqtt = True
mqtt_dict = {'topic': b'/will/client', 'last_will': b'dead', 'broker_address': '139.129.200.70', 'broker_port': 9883, 'mqtt_user': None, 'mqtt_password': None}


#beat heart config
beat_heart = False
beat_heart_dict = {'heart_address': '139.129.200.70', 'heart_port': 9997, 'heart_content': '-B', 'interval': 4}


#UART config
uart1 = False
uart1_dict = {"tx":33,"rx":32,"baudrate":115200,"data_bits":8,"stop_bits":1,"parity":None}

uart2 = True
uart2_dict = {'tx': 17, 'rx': 16, 'baudrate': 115200, 'data_bits': 8, 'stop_bits': 1, 'parity': None}
modbus_rtu_list = [{'device': 'u001', 'slave_id': 1, 'address': 0, 'quantity': 10, 'function': '03', 'timeout': 5, 'lora': False, 'mqtt': True}, {'device': 'u002', 'slave_id': 2, 'address': 0, 'quantity': 10, 'function': '03', 'timeout': 5, 'lora': False, 'mqtt': True}]

#modbus tcp
modbus_tcp = True
modbus_tcp_dict = {'device': '005', 'ip': '192', 'port': 2, 'slave_id': 3, 'address': 4, 'quantity': 5, 'function': '02', 'timeout': 5, 'lora': True, 'mqtt': False}
modbus_tcp_list = [{'device': '001', 'ip': '192.168.3.2', 'port': 502, 'slave_id': 1, 'address': 0, 'quantity': 10, 'function': '03', 'timeout': 5, 'lora': False, 'mqtt': True}, {'device': '002', 'ip': '192.168.2.4', 'port': 6001, 'slave_id': 1, 'address': 0, 'quantity': 10, 'function': '03', 'timeout': 5, 'lora': False, 'mqtt': True}, {'device': '004', 'ip': '192.23.2.33', 'port': 6001, 'slave_id': 1, 'address': 2, 'quantity': 10, 'function': '02', 'timeout': 5, 'lora': False, 'mqtt': True}]

lora = False
lora_mode = 2  #1=transmitter, 2=receiving ,3=morse transimit,4=beeper
lora_frequency = 433000
high_power = True  #add +3 dB (up to +20 dBm power on PA_BOOST pin)

lora_receive_mode = True
lora_receive_dict = {'frequency': 435000, 'mqtt': True, 'uart2': False}
