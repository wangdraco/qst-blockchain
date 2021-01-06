import paho.mqtt.client as mqtt #import the client1
import json,time
#broker_address="222.175.118.138"
broker_address="139.129.200.70"
#broker_address="47.104.196.27"
broker_port = 9883

#实时查看当前断路器状态
status_topic = '/b03b99VXEV1/5c7778354c1d6f180cc991d4/status/update'
_data = {}
_data['Device'] = '5c7778354c1d6f180cc991d4'  # controllerID
_datalist = []
_datalistdict = {}
_datalistdict['LineNo'] = 0
_datalistdict['Status'] = 0
_datalist.append(_datalistdict)

_data['Lines'] = _datalist

status_payload = json.dumps(_data,ensure_ascii=False)

setting_topic = '/b03b99VXEV1/5c7778354c1d6f180cc991d4/setting/update'
temp_setting = {}
temp_setting['Device'] = '5c7778354c1d6f180cc991d4'
temp_setting['LineNo'] = 5
temp_setting['Key'] = 'max_current'
temp_setting['Value'] = 40

_payload = json.dumps(temp_setting,ensure_ascii=False)
#_payload = 'close1'


temp_setting['LineNo'] = 4
temp_setting['Key'] = 'max_voltage'
temp_setting['Value'] = 235
_payload = json.dumps(temp_setting,ensure_ascii=False)
#broker_address="iot.eclipse.org" #use external broker
client = mqtt.Client(client_id='draco33') #create new instance
client.enable_logger()
try:
    client.connect(broker_address,broker_port) #connect to broker
except Exception as err:
    print('error===========',err)

while 1:

    #client.publish(status_topic,status_payload,qos=1,retain=False)#publish
    client.publish('/will/client','this a test message',qos=1,retain=False)
    client.publish('/ac67b207e6a0/sub/update', 'this a test message', qos=1, retain=False)
    #print('publish payload is =========',_payload)
    time.sleep(20)
#client.disconnect()