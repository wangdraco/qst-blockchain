import socketserver
from app import  mc

class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(2048).strip()
        print("{} wrote:".format(self.client_address[0]))
        #print(self.data)
        print(str(self.data, "utf-8"))
        if str(self.data, "utf-8").endswith('}]}'): #得到的json是完整的
            mc.set('zthr-hr-day',str(self.data, "utf-8"))
        # just send back the same data, but upper-cased
        #self.request.sendall(self.data.upper())

def run_tcpserver():
    (HOST, PORT) = '127.0.0.1', 5001

    # Create the server, binding to localhost on port 9999
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()


if __name__ == "__main__":
    (HOST, PORT) = "192.168.1.7", 9997

    # Create the server, binding to localhost on port 9999
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()