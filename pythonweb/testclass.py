import json
class Test:
    def __init__(self,_name = 'draco',_age=23):
        self.name = _name
        self.age = _age
        self.sex = '00'



t = Test()
print(json.dumps(t.__dict__,sort_keys=True))

import json
a = [{1:1,"a":"a"}, {2:3,"b":"b"}]
b = json.dumps(a)
c = json.loads(b)
print(b,type(b))
print(c,type(c))

def str_to_hex(s):
    return ''.join([hex(ord(c)).replace('0x', '') for c in s])
print(str_to_hex('list\\000.xkl'))

