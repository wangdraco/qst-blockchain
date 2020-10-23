esp32-WROOM-32模组
LoRa使用的是安信可的RA-02,sx1278模组

管脚说明

GPIO22  ---> LoRa  reset
GPIO21  ---> LoRa  DIO0
GPIO15  ---> LoRa  NSS/SPI CS
GPIO14  ---> LoRa  SLCK
GPIO13  ---> LoRa  MOSI
GPIO12  ---> LoRa  MISO

GPIO27  ---> 硬件看门狗

GPIO25 ---> UART1-TXD   #调整为32
GPIO26  ---> UART1-RXD  #调整为33

GPIO16  ---> UART2-RXD
GPIO17  ---> UART2-TXD

GPIO2  ---> LoRa的收发信号灯
GPIO19  ---> UART RX灯
GPIO18  ---> UART TX灯

GPIO5  --->  初始化按钮

1,inisetup.py是自带的文件，用于生成boot.py或其他文件，现在让他生成了config.py
  所以每次生成firmware的时候,先修改这个文件

2,闪烁用法
  from blink_class import blink
  blink(2) #让gpio2连接的灯闪烁
  blink(2,100) #闪烁100次
