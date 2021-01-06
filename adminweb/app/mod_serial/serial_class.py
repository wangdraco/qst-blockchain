import serial,time

class SerialClass:
    def __init__(self,_port, _baudrate, _parity, _stopbits, _bytesize):
        self.port = _port
        self.baudrate = _baudrate
        self.parity = _parity
        self.stopbits = _stopbits
        self.bytesize = _bytesize

    def loop_readline(self):
        while True:
            try:
                with serial.Serial(self.port, baudrate=self.baudrate, parity=self.parity,
                                   stopbits=self.stopbits, bytesize=self.bytesize, timeout=2) as ser:
                    line = ser.readline()
                    if line:
                        print('before ',line)
                        print('serial data is,', line.decode(), '--', len(line))
                    time.sleep(1)
            except Exception as e:
                print('read serial error:', e)
                time.sleep(5)
    def write_line(self,payload):
        try:
            with serial.Serial(self.port, baudrate=self.baudrate, parity=self.parity,
                               stopbits=self.stopbits, bytesize=self.bytesize) as ser:

                ser.write(payload.encode())
        except Exception as e:
            print('write serial error:', e)
            time.sleep(5)

if __name__ == '__main__':
    s = SerialClass('COM1',115200,'N',1,8)
    # s.loop_readline()
    s.write_line('testfdsfasfsdfdsfdsf\n')

