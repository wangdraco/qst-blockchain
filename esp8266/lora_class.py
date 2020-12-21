# -*- coding: UTF8 -*-
import gc
import config
import sx127x
gc.collect()

# implicit header (LoRa) or fixed packet length (FSK/OOK)
# FIXED = True
FIXED = False

class LoRa:

    def __init__(self):
        self.tr = sx127x.RADIO(mode=sx127x.LORA)
        self.u_id = config.mac_id

        self.tr.setFrequency(config.lora_frequency, 000)  # kHz, Hz
        self.tr.setPower(10, True)  # power dBm (RFO pin if False or PA_BOOST pin if True)
        self.tr.setHighPower(config.high_power)  # add +3 dB (up to +20 dBm power on PA_BOOST pin)
        self.tr.setOCP(120, True)  # set OCP trimming (> 120 mA if High Power is on)
        self.tr.enableCRC(True, True)  # CRC, CrcAutoClearOff (FSK/OOK mode)
        self.tr.setPllBW(2)  # 0=75, 1=150, 2=225, 3=300 kHz (LoRa/FSK/OOK)

        if self.tr.isLora():  # LoRa mode
            self.tr.setBW(250.)  # BW: 7.8...500 kHz
            self.tr.setCR(8)  # CR: 5..8
            self.tr.setSF(10)  # SF: 6...12
            self.tr.setLDRO(False)  # Low Datarate Optimize
            self.tr.setPreamble(6)  # 6..65535 (8 by default)
            self.tr.setSW(0x12)  # SW allways 0x12

        else:  # FSK/OOK mode
            self.tr.setBitrate(4800)  # bit/s
            self.tr.setFdev(5000.)  # frequency deviation [Hz]
            self.tr.setRxBW(10.4)  # 2.6...250 kHz
            self.tr.setAfcBW(2.6)  # 2.6...250 kHz
            self.tr.enableAFC(True)  # AFC on/off
            self.tr.setFixedLen(False)  # fixed packet size or variable
            self.tr.setDcFree(0)  # 0=Off, 1=Manchester, 2=Whitening

        #self.tr.dump()
        self.tr.collect()

    def send(self,_payload):

        self.tr.blink()
        print('send messages is ====--{}---{}'.format(self.u_id,_payload))
        self.tr.send(self.u_id + "$" + _payload, FIXED)

    def on_receive(self,tr, payload, crcOk):
        tr.blink()
        payload_string = payload.decode()
        # payload_string = str(payload)
        rssi = tr.getPktRSSI()
        snr = tr.getSNR()
        print("*** Received message:")
        print(payload_string)
        print("^^^ CrcOk={}, size={}, RSSI={}, SNR={}\n".format(crcOk, len(payload), rssi, snr))

    def receive(self):
        # reseiver
        self.tr.onReceive(self.on_receive)  # set the receive callback

        # go into receive mode
        if FIXED:
            self.tr.receive(6)  # implicit header / fixed size: 6=size("Hello!")
        else:
            self.tr.receive(0)  # explicit header / variable packet size

        #警告，放到协程里后， 这行可以屏蔽掉了，协程也是在一个while循环里!!!
        #time.sleep(-1)  # wait interrupt

    async def lora_receive_task(self,_point, time_ms):
        import uasyncio as asyncio
        while True:
            try:
                self.receive()
            except Exception as e:
                print('lora receive  error-------------------', e)
            await asyncio.sleep(time_ms)




