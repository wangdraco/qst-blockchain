# -*- coding: UTF8 -*-
# active access point function in a thread...
import _thread

def activeAP():
    import network
    import config as conf
    ap_if = network.WLAN(network.AP_IF)
    ap_if.active(conf.ap_mode)
    ap_if.config(essid=conf.ap_essid, authmode=network.AUTH_WPA_WPA2_PSK, password=conf.ap_password)

_thread.start_new_thread(activeAP, ())