import _thread,time,struct

def test_print(s,t):
    while True:
        print('hello------')
        time.sleep(s)

try:
    _thread.start_new_thread(test_print, (2,2))
except Exception as e:
    print(e)


_b = (b'{"demfj#\xac\xb8\x1ek\xa0\xf8\xeao\x8eJ\xcd\xee\x9em\x8aJ\x81\\\xe2\xe1\x08a\x96\x7f\xb9+\x04J\xc6\xd4\x8bi\x99g\x8ex\x01x\xc0|(\xfaVo\xa1\x1e\xbe\nH\xbc\xf3\x9fh\x85b/\x03\n')
_s = '{"devId":"3E0069000550505958353820","temp":"29.30","humi":"16.19"}'
_ss = "demfj#\xac\xb8\x1ek\xa0\xf8\xeao\x8eJ\xcd\xee\x9em\x8aJ\x81\\\xe2\xe1\x08a\x96\x7f\xb9+\x04J\xc6\xd4\x8bi\x99g\x8ex\x01x\xc0|(\xfaVo\xa1\x1e\xbe\nH\xbc\xf3\x9fh\x85b/\x03\n"
print(len(_b))
# print(struct.unpack('BBBBB', bytes(['xb8',49,49,49,49])))
print(bytearray('111111111'.encode('ascii')))


