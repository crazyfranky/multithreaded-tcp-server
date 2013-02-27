import socket
import sys
import threading
import random
import os

###

HOST = "0.0.0.0"
PORT = 8989
SOCK_ADDR = (HOST, PORT)

###

class SocketClientObject(object):

    def __init__(self, socket, address ):
        self.socket = socket
        self.address = address

###

class ClientThread(threading.Thread):
    
    def __init__(self, client_object):
        threading.Thread.__init__(self)
        self.client_object = client_object

    def run(self):
        data = self.client_object.socket.recv(1024)
        print ">> Received data: ", data, " from: ", self.client_object.address
        self.client_object.socket.sendall("qqq")
        self.client_object.socket.close()

###

def main():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(SOCK_ADDR)
        sock.listen(5)
        while 1:
            # accept connections from outside
            (clientsocket, address) = sock.accept()
            print "# Accept client: ", address
            # now do something with the clientsocket
            # in this case, we'll pretend this is a threaded server
            ct = ClientThread( SocketClientObject( clientsocket, address ) )
            ct.start()
    except:
        print "#! EXC: ", sys.exc_info()
        sock.close()
        print "THE END! Goodbye!"

###

if __name__ == "__main__":
    main()
