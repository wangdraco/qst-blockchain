import socket
import time,threading,schedule
from socketserver import TCPServer, StreamRequestHandler


__author__ = 'Draco.Wang'

class MyStreamRequestHandlerr(StreamRequestHandler):
    def __init__(self, request, client_address, server):
        print('%s create handler...' % (time.time()))
        StreamRequestHandler.__init__(self, request, client_address, server)

    def handle(self):
        self.request.settimeout(0)
        try:
            self.data = self.rfile.readline().strip()
            print(f"{self.request} wrote:".format(self.client_address[0]))
            # print(self.data)
            print(type(self.data), ' received value is ', str(self.data, "utf-8"))
            # data = self.rfile.readline().strip()
            # time.sleep(5)
            print('%s recv from client: %s %s' % (time.time(), self.client_address, self.data))
        except socket.timeout as e:
            print('%s catch an timtout exception. %s(%s)' % (time.time(), e, self.client_address))
            self.finish()


class SimpleServer(TCPServer):
    # timeout = 2
    def __init__(self, server_address, RequestHandlerClass):
        # self.timeout = 2
        TCPServer.__init__(self, server_address, RequestHandlerClass)

    def handle_timeout(self):
        print('%s timeout...' % time.time())


def main():
    server = SimpleServer(('127.0.0.1', 30000), MyStreamRequestHandlerr)
    server.timeout = 2
    print('server running...')
    # server.serve_forever()
    while True:
        server.handle_request()
        time.sleep(1)
    # process_socket_server()