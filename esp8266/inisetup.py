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
    with open("boot.py", "w") as f:
        f.write(
            """\
# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()

import feeddog
"""
        )

    with open("config.py", "w") as f:
        f.write(
            """\
import ubinascii,machine
mac_id = str(ubinascii.hexlify(machine.unique_id()),'utf-8')


#gc collect
gc_collect = True

sta_mode = True
# SSID = 'tw-gelou'
# PASSWORD = 'netgear168'

SSID = 'HUAWEI-400Q0S'
PASSWORD = 'zhimakaimen1203'

#enable Access Point mode
#ap_if = network.WLAN(network.AP_IF)
#ap_if.active(True)
#ap_if.config(essid="yunwei-lora",channel=11,password="")
ap_mode = True
ap_essid = "lora"+mac_id
ap_password = "yunwei168"

#mqtt config
mqtt = False
topic = b'/will/client'
last_will = b'dead'
broker_address = '139.129.200.70'
broker_port = 9883
mqtt_user = None
mqtt_password = None

#beat heart config
beat_heart = True
heart_address = '139.129.200.70'
heart_port = 9997
heart_content = mac_id+"-"+"bbb"

#UART config
uart1 = False
uart1_dict = {"tx":25,"rx":26,"baudrate":115200,"data_bits":8,"stop_bits":1,"parity":None}

uart2 = True
uart2_dict = {"tx":17,"rx":16,"baudrate":115200,"data_bits":8,"stop_bits":1,"parity":None}

#modbus tcp
modbus_tcp = True
modbus_tcp_dict = {"ip":"139.129.200.70","port":9996,"timeout":5}

lora=False
lora_mode = 2  #1=transmitter, 2=receiving ,3=morse transimit,4=beeper
lora_frequency = 433000
high_power = True  #add +3 dB (up to +20 dBm power on PA_BOOST pin)
"""
        )

    return vfs
