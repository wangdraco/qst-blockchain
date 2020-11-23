
## -*- coding: utf-8 -*-
from machine import UART ,Pin ,Timer
import utime

from collections import OrderedDict

uart = UART(1, baudrate=115200, tx=33, rx=32, bits=8, parity=None, stop=1)

command_dict = OrderedDict()

#开机初始化的at命令
command_dict["AT"] = "ERROR"
command_dict["ATE0"] = "ERROR"
command_dict["AT+WAKETIM=0"] = "ERROR"
command_dict["AT&W"] = "ERROR"
command_dict["AT+CIMI"] = "ERROR"
command_dict["AT+CSQ"] = "+CSQ:99,99"
command_dict["AT+CEREG?"] = "+CEREG: 0,0"
command_dict["AT+CGATT?"] = "+CGATT: 0"

#MQTT连接命令
mqtt_dict =  OrderedDict()
mqtt_dict["AT+CGREG?"] = "+CGREG: 0,1" #先查询当前GPRS注册状态看是否断网
mqtt_dict["AT+CGATT?"] = "+CGATT: 1" #查看当前GPRS附着状态

mqtt_dict["AT+MCONFIG={},{},{}".format("test_cat4G_mqtt","","")] = "OK" # 设置MQTT相关参数:AT+MCONFIG="clientid","account","password"
mqtt_dict["AT+MIPSTART={},{}".format("139.129.200.70","9883")]  = "OK"#建立TCP 连接
mqtt_dict["AT+MCONNECT=1,300"] = "OK" # 客户端向服务器请求会话连接：AT+MCONNECT

mqtt_dict["AT+MSUB={},1".format("/will/client")] = "OK" #订阅主题

#发布消息 AT+MPUB=<topic>,<qos>,<retain> ,<message>,message必须是双引号
mqtt_dict['AT+MPUB={},{},{},"{}"'.format("/will/client",1,0,"this a test message from cat4G")] = "OK"
def run_at_mqtt(_uart ,_command ,_return):
    count = 1
    _uart.write(_command + "\r\n")
    utime.sleep_ms(1000)
    while True:
        if _uart.any():
            _r = _uart.read().decode()
            # print("-----------"+_r)
            if _return in _r:
                result = "command :{} is {}".format(_command, _r.replace("\r\n", ""))
                break
            else:
                uart.write(_command + "\r\n")
                utime.sleep_ms(1000)
                count += 1

        if count == 2:
            result = "command :{} is {}".format(_command, _return)
            break
    print(result)


def run_at_command(_uart ,_command ,_return):

    count = 1
    _uart.write(_command +"\r\n")
    utime.sleep_ms(1000)
    while True:
        if _uart.any():
            _r = _uart.read().decode()
            # print("-----------"+_r)
            if _return in _r:
                uart.write(_command + "\r\n")
                utime.sleep_ms(1000)
                count += 1
            else:
                result = "command :{} is {}".format(_command, _r.replace("\r\n" ,""))
                break

        if count == 3:
            result = "command :{} is {}".format(_command, _return)
            break
    print(result)

def run_initial():
    print("begin initialization........")
    for k, v in command_dict.items():
        run_at_command(uart, k, v)

def run_mqtt():
    print("begin MQTT........")
    for k, v in mqtt_dict.items():
        run_at_mqtt(uart, k, v)

run_mqtt()



