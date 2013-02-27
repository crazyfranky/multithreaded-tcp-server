import socket
import sys
import threading
import random
import os

###

HOST = "0.0.0.0"
PORT = 110
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
        self.running = 0
        self.user_login = ''
        self.user_pass = ''
        self.command_handlers = {'USER': self.USER_handler,
                                 'PASS': self.PASS_handler,
                                 'STAT': self.STAT_handler,
                                 'QUIT': self.QUIT_handler}

###

    def USER_handler(self, cmd_data):
        self.user_login = cmd_data.split(" ")[1].replace('\r','').replace('\n','')
        print self.user_login
        self.client_object.socket.send("+OK " + self.user_login + "... User ok\r\n")

    def PASS_handler(self, cmd_data):
        if not self.user_login:
            return
        self.user_pass = cmd_data.split(" ")[1].replace('\r','').replace('\n','')
        print self.user_login, self.user_pass
        self.client_object.socket.send("+OK " + self.user_login + "'s mailbox has 0 total messages (0 octets)\r\n")

    def STAT_handler(self, cmd_data):
        self.client_object.socket.send("+OK 0 0\r\n")

    def QUIT_handler(self, cmd_data):
        self.client_object.socket.send("+OK " + self.user_login + " host.local POP3 Server signing off (mailbox empty)\r\n")
        self.running = 0

###

    def run(self):
        self.client_object.socket.send("+OK host.local POP3 MDaemon 11.0.3 ready <MDAEMON-1103@host.local>\r\n")
        self.running = 1
        while self.running:
            resp = self.client_object.socket.recv(1024)
            print ">> Received data: ", resp, " from: ", self.client_object.address
            cmd = resp[:4]
            cmd_handler = self.command_handlers.get(cmd, None)
            if not cmd_handler:
                break
            cmd_handler(resp)
            sys.stdout.flush()
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
