import socket
import json
import sys
import logging as logi
from Connector import Connector

C = Connector()

address = 'localhost'
if len(sys.argv) == 2:
    address = sys.argv[1]
server = (address,5555)

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.connect(server)

size = 1024
try:
    print "Connecting..."
    while True:
        data = sock.recv(size)
        data = data.strip().split()
        if len(data) != 5 or len(data[0]) != 10 or len(data[1]) != 9:
            continue
        print "Recieve task : {} {} {} {} {}".format(data[0],data[1],data[2],data[3],data[4])
        receipt = C.Task(data[0],data[1],int(data[2]),int(data[3]),int(data[4]))
        sock.sendall(json.dumps(receipt))
        print "Task done!!"
except Exception as e:
    print e
    sock.close()
