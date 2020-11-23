# -*- coding: UTF8 -*-
# Micropython global config files
# Author: Draco.Wang <1599980410@qq.com>
import config as conf
class WiFi:

    def __init__(self,ssid = conf.SSID, password = conf.PASSWORD):
        self.SSID = ssid
        self.PASSWORD = password
    def connect(self):
        import network

        sta = network.WLAN(network.STA_IF)

        if not sta.isconnected():
            try:
                sta.active(True)
                sta.scan()
                sta.connect(self.SSID, self.PASSWORD)
            except Exception as e:
                print('connect error !!!!',e)
        print('network config:', sta.ifconfig())
        return sta