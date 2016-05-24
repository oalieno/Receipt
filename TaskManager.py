import socket
import json
import sys
import Queue
import logging as log
from TimeConvert import TimeConvert
from DBManager import DBManager
from TaskDBManager import TaskDBManager

class TaskManager(object):
    def __init__(self):
        self.dbmanager = DBManager()
        self.taskdbmanager = TaskDBManager()
    
    def Connect(self):
        server = ('localhost',5555)
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sock.connect(server)

    def AssignTask(self,number,date,direction,shift,distance):
        success = 0
        datemodify = 0
        try:
            self.sock.sendall("{} {} {} {} {}".format(number,date,str(direction),str(shift),str(distance)))
            data = self.sock.recv(4096)
            try:
                receipt = json.loads(data)
            except:
                print data
            log.debug(data)
            if len(receipt) >= distance-5:
                success = 1
            if receipt.get(number[0:2]+str(int(number[2:])+shift+distance-1),date)[0] != date:
                datemodify = direction
            self.dbmanager.StoreData(receipt)
        except socket.error as e:
            self.Close()
            print "shit happened {}".format(e)    
        return success,datemodify

    def Close(self):
        self.sock.close()
   
    def Run(self):
        q = Queue.Queue()
        data = self.taskdbmanager.GetData()
        for i in data:
            i = (i[0].encode('ascii','ignore'),i[1].encode('ascii','ignore'),i[2],i[3],i[4])
            q.put(i)
        try:
            while not q.empty():
                wow = q.get()
                print "Assign Task:{} {} {} {} {}".format(wow[0],wow[1],wow[2],wow[3],wow[4])
                s,d = self.AssignTask(wow[0],wow[1],wow[2],wow[3],wow[4])
                if s:
                    print "Success!!Add new Task~"
                    q.put((wow[0],TimeConvert(wow[1],d),wow[2],wow[3]+wow[4],wow[4]))
                else:
                    print "Fail!!Reach the end!!"
            else:
                self.taskdbmanager.Clear()
                print "=====All done====="
        except:
            L = []
            while not q.empty():
                L.append(q.get())
            print L
            self.taskdbmanager.Clear()
            self.taskdbmanager.StoreAll(L)
            print "=====Task Saved====="

if __name__ == '__main__':
    #log.basicConfig(level = log.DEBUG)
    T = TaskManager()
    T.Connect()
    T.Run()
    #T.AssignTask("HB22675221","105/05/15",1,0,10)
    T.Close()
