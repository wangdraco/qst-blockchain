import config as conf
import usocket as socket

class HeartBeat:
    def __init__(self):
        self.address = conf.beat_heart_dict['heart_address']
        self.port = conf.beat_heart_dict['heart_port']
        self.heart_content = conf.beat_heart_dict['heart_content']
    def send(self,_content=conf.mac_id+'-B'):
        sock = socket.socket()
        sock.connect((self.address, self.port))
        sock.send(_content.encode('utf-8'))  # data+'\n'
        received = str(sock.recv(128), "utf-8")
        print('send beat ', _content," and get ",received)
        sock.close()
        return received