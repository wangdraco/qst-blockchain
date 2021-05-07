# coding: utf-8
import socket
import time
from socketserver import TCPServer, StreamRequestHandler
from app import client_socket

class MyStreamRequestHandlerr(StreamRequestHandler):

    channel = None

    def __init__(self, request, client_address, server):
        print('%s create handler...' % (time.time()))

        StreamRequestHandler.__init__(self, request, client_address, server)
    def handle(self):
        self.request.settimeout(0)#可以设置客户响应超时
        try:
            self.data = self.rfile.readline().strip()
            print("{} wrote:".format(self.client_address[0]))
            if MyStreamRequestHandlerr.channel:
                _sock = {}
                _sock['time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
                _sock['status'] = True
                _sock['sock'] = self.request
                client_socket['gprs-socket' + str(MyStreamRequestHandlerr.channel.port)] = _sock
                print(f'{MyStreamRequestHandlerr.channel} in handle() received value is ', str(self.data, "utf-8"), ' channel=',_sock)

            print('%s recv from client: %s %s' % (time.time(), self.client_address, self.data))
            #可以设置回写
            #self.wfile.write(self.data)
        except socket.timeout as e:
            print('%s catch an timtout exception. %s(%s)' % (time.time(), e, self.client_address))
            self.finish()

class GprsServer(TCPServer):#适用于2g，3G，4G等无线网络
    def __init__(self, server_address, RequestHandlerClass):
        # self.timeout = 2
        self.channel = None
        TCPServer.__init__(self, server_address, RequestHandlerClass)

    def handle_timeout(self):
        print('%s timeout...' % time.time(),' ',self.channel)

def main():
    MyStreamRequestHandlerr.channel = '33333333333'
    server = GprsServer(('127.0.0.1', 30000), MyStreamRequestHandlerr)
    server.channel = 'fdsfsdfsdfsd'
    server.timeout = 2 #设置等待客户连接时间，超过2秒，说明没有客户连接，调用handle_timeout
    print('server running...')
    # server.serve_forever()
    while True:
        server.handle_request()
        time.sleep(2)

if '__main__' == __name__:
    main()