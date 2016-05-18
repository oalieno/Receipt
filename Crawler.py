import socket
import cPickle as pickle
import logging as log
from Connector import Connector

C = Connector()

host = 'localhost'
port = 5555

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((host,port))
s.listen(1)

while True:
    connection,address = s.accept()
    try:
        log.debug("Connect to {}".format(address))
        while True:
            data = connection.recv(256)
            if data:
                _data = data.strip().split()
                if len(_data) != 3:
                    connection.sendall("=====Wrong Format=====\nShould be(ReceiptId,Date,HowMany)\n")
                    continue
                log.debug("Recieve task : {} {} {}".format(_data[0],_data[1],_data[2]))
                receipt = C.Task(_data[0],_data[1],int(_data[2]))
                connection.sendall(pickle.dumps(receipt,-1))
            else:
                print "no more data"
                break
        connection.close()
        break
    except:
        print "error happened shit happened"
        connection.close()
        break
