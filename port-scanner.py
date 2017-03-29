#!/usr/bin/python
import socket
import sys, errno




class Client:
    def __init__(self,sock=None):
        if sock is None:
            self.sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock=sock

    def connect(self, host, port):
        return self.sock.connect_ex((host,port))
    def mysend(self,msg):
        MSGLEN = 1
        totalsent = 0
        while totalsent < MSGLEN:
            sent = self.sock.send(msg[totalsent:])
            if sent == 0 :
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent
    def myreceive(self):
        chunks = []
        bytes_recd = 0
        MSGLEN = int(self.sock.recv(1))
        while bytes_recd < MSGLEN:
            chunk = self.sock.recv(min(MSGLEN - bytes_recd, 2048))
            if chunk == '':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
        return ''.join(chunks)

if __name__ == '__main__':
    client = Client()
    ports = []
    if len(sys.argv) == 3:
        server_address = sys.argv[1]
        server_port = sys.argv[2]
    else:
        exit(errno.EINVAL)
    client.connect(server_address,int(server_port))
    tserver_port = client.myreceive()
    while tserver_port != '':
        tserver_port = client.myreceive()
        tclient = Client()
        if(tclient.connect(server_address, int(tserver_port)) == 0):

            print tserver_port
            ports.append(tserver_port)
    print '| '.join(ports)




