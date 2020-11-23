esp32-WROOM-32模组
LoRa使用的是安信可的RA-02,sx1278模组

管脚说明（基础版本，lora+wifi）

GPIO22  ---> LoRa  reset
GPIO21  ---> LoRa  DIO0
GPIO15  ---> LoRa  NSS/SPI CS
GPIO14  ---> LoRa  SLCK
GPIO13  ---> LoRa  MOSI
GPIO12  ---> LoRa  MISO

GPIO27  ---> 硬件看门狗

GPIO25 ---> UART1-TXD   #调整为33
GPIO26  ---> UART1-RXD  #调整为32

GPIO16  ---> UART2-RXD
GPIO17  ---> UART2-TXD

GPIO2  ---> LoRa的收发信号灯
GPIO19  ---> UART RX灯
GPIO18  ---> UART TX灯

GPIO5  --->  初始化按钮


管脚说明（中级版本，lora+wifi+cat1）
GPIO2  ---> LoRa的收发信号灯

外部485灯
GPIO23  ---> UART RX灯
GPIO26  ---> UART TX灯




1,inisetup.py是自带的文件，用于生成boot.py或其他文件，现在让他生成了config.py
  所以每次生成firmware的时候,先修改这个文件

2,闪烁用法
  from blink_class import blink
  blink(2) #让gpio2连接的灯闪烁
  blink(2,100) #闪烁100次


关于4M版本的esp32的分区问题
分为： partitions.csv工厂程序（无OTA分区）/
       partitions-ota.csv工厂程序（双OTA分区）/
       用户自定义分区

原始的~/esp/micropython/ports/esp32/partitions.csv文件如下：
# Notes: the offset of the partition table itself is set in
# $ESPIDF/components/partition_table/Kconfig.projbuild and the
# offset of the factory/ota_0 partition is set in makeimg.py
# Name,   Type, SubType, Offset,  Size, Flags
nvs,      data, nvs,     0x9000,  0x6000,
phy_init, data, phy,     0xf000,  0x1000,
factory,  app,  factory, 0x10000, 0x180000,
vfs,      data, fat,     0x200000, 0x200000,

我们可以看到：
定义了两个用于存储 NVS 库分区和 PHY 初始化数据的数据区域
在0x10000(64 KB) 偏移量处为 factory 应用程序(即固件大小)，定义的长度是0x180000,大约是 1.5 M
vfs是数据区，也就是根目录，存放程序文件的空间


如果固件firmware.bin文件太大，超过2M，则使用下面的

# Name,   Type, SubType, Offset,  Size, Flags
nvs,      data, nvs,     0x9000,  0x6000,
phy_init, data, phy,     0xf000,  0x1000,
factory,  app,  factory, 0x10000, 0x200000,
vfs,      data, fat,     0x220000, 0x170000,

具体参照： https://blog.csdn.net/toopoo/article/details/107327828