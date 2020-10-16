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

GPIO25 ---> UART1-TXD
GPIO26  ---> UART1-RXD

GPIO16  ---> UART2-RXD
GPIO17  ---> UART2-TXD

GPIO2  ---> LoRa的收发信号灯
GPIO19  ---> UART RX灯
GPIO18  ---> UART TX灯

GPIO5  --->  初始化按钮
