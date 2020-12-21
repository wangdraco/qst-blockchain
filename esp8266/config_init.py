import ubinascii,machine
mac_id = str(ubinascii.hexlify(machine.unique_id()),'utf-8')

#gc collect
gc_collect = True

#timer ,restart time
restart = True
restart_time = 21600000 #6 hours

#hardware watchdog
watchdog = True

#web username&password
web_server = False
web_username = 'admin'
web_password = '1234'

sta_mode = False
SSID = 'wifi-ssid'
PASSWORD = 'wifi-password'

# SSID = 'HUAWEI-400Q0S'
# PASSWORD = 'zhimakaimen1203'


ap_mode = True
ap_essid = "lora-"+mac_id
ap_password = "yunwei168"

#run asyncio tasks in main.py
main_run = False

#mqtt config
mqtt = False
mqtt_dict = {'topic': b'/will/client','sub_topic':'/{}/sub/update'.format(mac_id).encode('utf-8'), 'last_will': b'dead', 'broker_address': '139.129.200.70', 'broker_port': 9883, 'mqtt_user': None, 'mqtt_password': None}

#beat heart config
beat_heart = False
heart_address = '139.129.200.70'
heart_port = 9997
heart_content = mac_id+"-"+"bbb"

#UART config
uart1 = False
uart1_dict = {"tx":33,"rx":32,"baudrate":115200,"data_bits":8,"stop_bits":1,"parity":None}

uart2 = False
uart2_dict = {"tx":17,"rx":16,"baudrate":115200,"data_bits":8,"stop_bits":1,"parity":None}
modbus_rtu_list = [{'device': 'u001', 'slave_id': 1, 'address': 0, 'quantity': 10, 'function': '03', 'timeout': 5, 'lora': False, 'mqtt': True}]

#modbus tcp
modbus_tcp = False
modbus_tcp_dict = {'device': '001', 'ip': '139.129.200.70', 'port': 502, 'slave_id': 1, 'address': 0, 'quantity': 10, 'function': '03', 'timeout': 5, 'lora': False, 'mqtt': True}
modbus_tcp_list = [{'device': '001', 'ip': '139.129.200.70', 'port': 502, 'slave_id': 1, 'address': 0, 'quantity': 10, 'function': '03', 'timeout': 5, 'lora': False, 'mqtt': True}]


lora=False
lora_mode = 2  #1=transmitter, 2=receiving ,3=morse transimit,4=beeper
lora_frequency = 433000
high_power = True  #add +3 dB (up to +20 dBm power on PA_BOOST pin)