import paho.mqtt.client as mqtt
import threading,time,json
from app.mod_redis.redis_class import Redis


class MqttLoraClass():
    def __init__(self,broker_address = "139.129.200.70",broker_port = 9883,topic = None, qos = 1,username='lora', password='lora1qaz',
                 socketio=None,client_id='', multiple_sub=False):
        self.broker_address = broker_address
        self.broker_port = broker_port
        self.client = mqtt.Client(client_id=client_id)
        self.client.username_pw_set(username,password)
        self.topic = topic
        self.qos = qos
        self.conn = False
        self.socketio = socketio
        self.multiple_sub = multiple_sub
        # self.mc = get_memcache()


    def on_connect(self,client,userdata,flag,rc):

        print("Connected ,rc=",rc)
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        self.conn = True

        #sub multiple topic
        if self.multiple_sub:
            self.client.subscribe(self.topic)
        else:
            self.sub_msg(self.topic,self.qos)

    def on_disconnect(self):
        print('disconnected from server...................')

    def on_message(self,client, userdata, msg):
        print(msg.topic + " " + str(msg.payload.decode('utf-8')))
        #write message to file or database
        t = threading.Thread(target=self.process_message,kwargs={'topic': msg.topic, 'content': str(msg.payload.decode('utf-8'))})
        t.start()

    def sub_msg(self,_topic, _qos):
        print('in submsg ===================',_topic,_qos)
        self.client.subscribe(_topic,_qos)

    def run_sub(self):
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect

        #self.client.connect(self.broker_address, self.broker_port, 60)

        #keepalive = 60 sec, check the con is alive every 60 seconds
        self.client.connect(self.broker_address, self.broker_port, 60)
        #self.client.loop_forever()
        #self.client.loop()
        self.client.loop_start()
        while 1:
            print('wait for ==========',self.topic)
            time.sleep(1)


    def run_pub(self,_payload):

        self.client.connect(self.broker_address, self.broker_port, 60)
        self.client.publish(self.topic, _payload, self.qos)  # publish

        #or in a loop for blocked data
        #while True
        #   temperature = sensor.blocking_read()
        #   self.client.publish(self.topic, temperature, self.qos)

    def process_message(self,**params):
        #write to redis
        if True: #根据配置文件来决定是否写入redis，一般是modbus设备的数据都有macid和deviceid，格式为macid$deviceID$result

            #有$的版本，需要用$来区分macid和deviceid
            # _payload = params['content']
            # mac_id = _payload[:_payload.index('$',0,len(_payload))]
            # r = Redis.connect()
            # if mac_id:
            #     device_id = _payload[_payload.index('$', 0, len(_payload)) + 1:_payload.rindex('$', 0, len(_payload))]
            #     result = _payload[_payload.rindex('$', 0, len(_payload)) + 1:]
            #     if device_id:
            #         r.hset(mac_id, device_id, result)
            #     else:
            #         r.hset(mac_id, '-', result)
            # else:#普通的数据
            #     r.set('lora-data',_payload)
            _payload = params['content']
            _payload = json.loads(_payload)
            mac_id = _payload.get('mac_id')
            r = Redis.connect()
            if mac_id:
                device_id = _payload.get('device')
                result = _payload.get('result')
                if device_id:
                    r.hset(mac_id, device_id, result)
                else:
                    r.hset(mac_id, '-', result)
            else:  # 普通的数据
                r.set('lora-data', params['content'])


def thread_sub(**topiclist):
    topic_list = topiclist['topic']

    m3 = MqttLoraClass(topic=topic_list, socketio=None, multiple_sub=True)
    m3.run_sub()



if __name__ == '__main__':


    topic_list = [("/lora/data/receive", 1),
                  ("/b03b99VXEV1/5c7778354c1d6f180cc991d4/leakage", 1)]
    tt = threading.Thread(target=thread_sub,kwargs={'topic': topic_list})
    tt.start()
    print('dddddddd')








