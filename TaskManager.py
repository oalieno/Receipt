import socket
import json
import logging as log
from DBManager import DBManager

class TaskManager(object):
    def __init__(self):
        self.dbmanager = DBManager()
    
    def Connect(self):
        server = ('localhost',5555)
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sock.connect(server)

    def AssignTask(self,number,date,direction,shift,distance):
        success = False
        try:
            self.sock.sendall("{} {} {} {} {}".format(number,date,str(direction),str(shift),str(distance)))
            data = self.sock.recv(4096)
            try:
                receipt = json.loads(data)
            except:
                print data
            log.debug(data)
            if len(receipt) == distance:
                success = True
            self.dbmanager.StoreData(receipt)
        except socket.error as e:
            self.Close()
            print "shit happened {}".format(e)    
        return success

    def Close(self):
        self.sock.close()

if __name__ == '__main__':
    #log.basicConfig(level = log.DEBUG)
    T = TaskManager()
    T.Connect()
    T.AssignTask("HB22675221","105/05/15",1,0,10)
    T.Close()
