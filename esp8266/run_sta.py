from wifi_class import WiFi
wifi = WiFi()
print('begin connect station is ==',wifi.SSID,'--',wifi.PASSWORD)
_sta = wifi.connect()