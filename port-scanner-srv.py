#!/usr/bin/python

import socket
import sys, errno
import threading
import time

class MainServer(threading.Thread):
    def __init__(self, server_port=443 , sock=None):
        threading.Thread.__init__(self)
        if sock is None:
            self.sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock=sock
        self.sock.bind((socket.gethostname(), server_port))
        self.sock.listen(1)
        self.clientsocket = None
        self.address = ''
        self.connectionsuccesfull = 0
    def run(self):
        while 1:
            try:
                (self.clientsocket, self.address) = self.sock.accept()
                self.connectionsuccesfull = 1
                self.sock.shutdown(socket.SHUT_RDWR)
                self.sock.close()
                break
            except:
                print "Socket was closed"
                break
    def mysend(self, msg):
        self.clientsocket.send(msg)
    def __del__(self):
        try:
            if self.clientsocket != None:
               self.sock.shutdown(socket.SHUT_RDWR)
        except:
            None
        self.sock.close()


class Client:
    def __init__(self,sock=None):
        if sock is None:
            self.sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock=sock
    def connect(self, host, port):
        self.sock.connect((host,port))



if __name__ == '__main__':
    ports = []
    if len(sys.argv) == 2:
        mainserver = MainServer(sys.argv[1])
    else:
        mainserver = MainServer()
        print "Using default port (443)"

    mainserver.start()
    while True:
        if mainserver.clientsocket != None:
            for i in range (1024, 65536):
                tserver = MainServer(i)
                tserver.start()
                mainserver.mysend(str(len(str(i))))
                mainserver.mysend(str(i))
                time.sleep(3)
                if tserver.connectionsuccesfull:
                    ports.append(str(i))
                    print str(i)
                else:
                    try:
                        ##This is needed to close the other thread if there is no legit connection
                        tclient = Client()
                        tclient.connect(socket.gethostname(), i)
                    except:
                        print "Unable to connect - port {}".join(i)
                    del tserver
            result = ', '.join(ports)
            mainserver.mysend("1") #sending length of next message
            mainserver.mysend("0") #sending signal for end of communication
            time.sleep(1)
            print result
            del mainserver
            break
    print "Finished execution"



