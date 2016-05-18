import socket
from Connector import Connector

host = 'localhost'
port = 5555

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((host,port))
s.listen(1)

C = Connector()

while True:
    connection,address = s.accept()
    try:
        print "Connect to",address
        while True:
            data = connection.recv(256)
            if data:
                _data = data.strip().split()
                if len(_data) != 4:
                    continue
                print _data
                money,hole = C.Task(_data[0],_data[1],int(_data[2]),int(_data[3]))
                connection.sendall("money : "+str(money)+" hole : "+str(hole))
            else:
                print "no more data"
                break
        connection.close()
        break
    except:
        print "error happened shit happened"
        connection.close()
        break
