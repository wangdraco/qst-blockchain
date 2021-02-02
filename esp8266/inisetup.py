import uos
from flashbdev import bdev


def check_bootsec():
    buf = bytearray(bdev.ioctl(5, 0))  # 5 is SEC_SIZE
    bdev.readblocks(0, buf)
    empty = True
    for b in buf:
        if b != 0xFF:
            empty = False
            break
    if empty:
        return True
    fs_corrupted()


def fs_corrupted():
    import time

    while 1:
        print(
            """\
FAT filesystem appears to be corrupted. If you had important data there, you
may want to make a flash snapshot to try to recover it. Otherwise, perform
factory reprogramming of MicroPython firmware (completely erase flash, followed
by firmware programming).
"""
        )
        time.sleep(3)


def setup():
    check_bootsec()
    print("Performing initial setup")
    uos.VfsLfs2.mkfs(bdev)
    vfs = uos.VfsLfs2(bdev)
    uos.mount(vfs, "/")

    with open("config.py", "w") as f:
        f.write(
            """\
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
web_server = True
web_username = 'admin'
web_password = '1234'

sta_mode = False
SSID = 'tw-gelou'
PASSWORD = 'netgear168'

# SSID = 'HUAWEI-400Q0S'
# PASSWORD = 'zhimakaimen1203'


ap_mode = True
ap_essid = "lora-"+mac_id
ap_password = "yunwei168"

#run asyncio tasks in main.py
main_run = False

#mqtt config
mqtt = False
mqtt_dict = {'topic': b'/lora/data/receive','sub_topic':'/{}/sub/update'.format(mac_id).encode('utf-8'), 'last_will': b'dead', 'broker_address': '139.129.200.70', 'broker_port': 9883, 'mqtt_user': 'lora', 'mqtt_password': 'lora1qaz'}

#beat heart config
beat_heart = False
beat_heart_dict = {'heart_address':'139.129.200.70', 'heart_port':9997, 'heart_content':'b','interval':3}

#UART config
uart1 = False
uart1_dict = {"tx":33,"rx":32,"baudrate":115200,"data_bits":8,"stop_bits":1,"parity":None}

uart2 = False
uart2_dict = {"tx":17,"rx":16,"baudrate":115200,"data_bits":8,"stop_bits":1,"parity":None}
modbus_rtu_list = [{'device': 'u001', 'slave_id': 1, 'address': 0, 'quantity': 10, 'function': '03', 'timeout': 5, 'lora': False, 'mqtt': True}, {'device': 'u002', 'slave_id': 2, 'address': 0, 'quantity': 10, 'function': '03', 'timeout': 5, 'lora': False, 'mqtt': True}]


#modbus tcp
modbus_tcp = False
modbus_tcp_dict = {'device': '001', 'ip': '139.129.200.70', 'port': 502, 'slave_id': 1, 'address': 0, 'quantity': 10, 'function': '03', 'timeout': 5, 'lora': False, 'mqtt': True}
modbus_tcp_list = [{'device': '001', 'ip': '192.168.3.2', 'port': 502, 'slave_id': 1, 'address': 0, 'quantity': 10, 'function': '03', 'timeout': 5, 'lora': False, 'mqtt': True}, {'device': '002', 'ip': '192.168.2.4', 'port': 6001, 'slave_id': 1, 'address': 0, 'quantity': 10, 'function': '03', 'timeout': 5, 'lora': False, 'mqtt': True}]


lora = False
lora_mode = 2  #1=transmitter, 2=receiving ,3=morse transimit,4=beeper
lora_frequency = 433000
high_power = True  #add +3 dB (up to +20 dBm power on PA_BOOST pin)

lora_receive_mode = False
lora_receive_dict = {'frequency': '433000', 'mqtt': False, 'uart2': False}
"""
        )
    with open("config_init.py", "w") as f:
        f.write(
                """\
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

ap_mode = True
ap_essid = "lora-"+mac_id
ap_password = "yunwei168"

#run asyncio tasks in main.py
main_run = False

#mqtt config
mqtt = False
mqtt_dict = {'topic': b'/lora/data/receive','sub_topic':'/{}/sub/update'.format(mac_id).encode('utf-8'), 'last_will': b'dead', 'broker_address': '139.129.200.70', 'broker_port': 9883, 'mqtt_user': 'lora', 'mqtt_password': 'lora1qaz'}

#beat heart config
beat_heart = False
beat_heart_dict = {'heart_address':'139.129.200.70', 'heart_port':9997, 'heart_content':'b', 'interval':3}


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

lora = False
lora_mode = 2  #1=transmitter, 2=receiving ,3=morse transimit,4=beeper
lora_frequency = 433000
high_power = True  #add +3 dB (up to +20 dBm power on PA_BOOST pin)

lora_receive_mode = False
lora_receive_dict = {'frequency': '433000', 'mqtt': False, 'uart2': False}
"""
        )

    with open("boot.py", "w") as f:
        f.write(
            """\
# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()
import config as conf
import machine
machine.freq(240000000)


#IRQ for init config.py
import handle_initconfig

if conf.watchdog:
    import feeddog

if conf.restart:
    import timer_task

if conf.sta_mode:
    import run_sta

#start ap mode
if conf.ap_mode:
    import run_ap

#start web server
if conf.web_server:
    import run_web
#import network
#import config as conf
#ap_if = network.WLAN(network.AP_IF)
#ap_if.active(conf.ap_mode)
#ap_if.config(essid=conf.ap_essid,authmode=network.AUTH_WPA_WPA2_PSK, password=conf.ap_password)

#generate web static files
import make_webfiles
"""
        )
    with open("modbus_data.py", "w") as f:
        f.write("""# -*- coding: UTF8 -*-""")


    return vfs
