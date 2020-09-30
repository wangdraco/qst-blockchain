# -*- coding: UTF8 -*-
# Micropython global config files
# Author: Draco.Wang <1599980410@qq.com>

class WiFi:

    def __init__(self):
        pass
    def connect(self):
        import network
        import config

        sta = network.WLAN(network.STA_IF)
        ap_if = network.WLAN(network.AP_IF)
        ap_if.active(config.ap_mode)
        ap_if.config(essid=config.ap_essid, channel=11, password=config.ap_password)
        if not sta.isconnected():
            try:
                sta.active(True)
                sta.scan()
                sta.connect(config.SSID, config.PASSWORD)
            except Exception as e:
                print('connect error !!!!',e)
        print('network config:', sta.ifconfig())