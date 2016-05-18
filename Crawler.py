import socket
import json
import logging as log
from Connector import Connector

C = Connector()

server = ('localhost',5555)

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.bind(server)
sock.listen(1)

while True:
    connection,address = sock.accept()
    try:
        log.debug("Connect to {}".format(address))
        while True:
            data = connection.recv(256)
            if data:
                _data = data.strip().split()
                if len(_data) != 3 or len(_data[0]) != 10 or len(_data[1]) != 9:
                    connection.sendall("=====Wrong Format=====\nShould be(ReceiptId,Date,HowMany)\n")
                    continue
                log.debug("Recieve task : {} {} {}".format(_data[0],_data[1],_data[2]))
                receipt = C.Task(_data[0],_data[1],int(_data[2]))
                connection.sendall(json.dumps(receipt))
            else:
                print "no more data"
                break
        connection.close()
        break
    except:
        print "error happened shit happened"
        connection.close()
        break
