# -*- coding: UTF8 -*-
import config as conf
from umqtt.simple import MQTTClient
import time

class Mqtt:

    def __init__(self,broker_address = conf.mqtt_dict["broker_address"],broker_port = conf.mqtt_dict["broker_port"],
                 topic=conf.mqtt_dict["topic"],sub_topic=conf.mqtt_dict['sub_topic'],last_will = conf.mqtt_dict["last_will"],client_id = conf.mac_id,
                 username = conf.mqtt_dict["mqtt_user"],password = conf.mqtt_dict["mqtt_password"]):
        self.broker_address = broker_address
        self.broker_port = broker_port
        self.topic = topic
        self.sub_topic = sub_topic
        self.last_will = last_will
        self.client_id = client_id
        self.username = username
        self.password = password
        self.client = MQTTClient(self.client_id, self.broker_address, port=self.broker_port,user=self.username, password=self.password)

    def pub(self,_payload):
        self.client.connect()
        self.client.publish(self.topic, str(self.client_id + '$' + _payload), qos=1)
        print('send MQTT message== ',str(self.client_id + '$' + _payload))
        self.client.disconnect()

    # Received messages from subscriptions will be delivered to this callback
    def sub_cb(self,topic, msg):
        print('get subscrip message =',(topic, msg))

    def sub(self,blocking = False):
        self.client.set_callback(self.sub_cb)
        self.client.connect()
        self.client.subscribe(self.sub_topic)
        while True:
            if blocking:
                # Blocking wait for message
                self.client.wait_msg()
            else:
                # Non-blocking wait for message
                self.client.check_msg()
                # Then need to sleep to avoid 100% CPU usage (in a real
                # app other useful actions would be performed instead)
                time.sleep(2)

        self.client.disconnect()


