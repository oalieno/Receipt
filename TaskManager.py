import socket
import threading
import json
import sys
import Queue
import time
import logging as log
from TimeConvert import TimeConvert
from DBManager import DBManager
from TaskDBManager import TaskDBManager

class TaskManager(object):
    def __init__(self):
        self.qdb = Queue.Queue()
        self.qdb_lock = threading.Lock()
        self.taskdbmanager = TaskDBManager()
        self.current = {}
        self.current_lock = threading.Lock()
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.sock.bind(('localhost',5555))
        self.q = Queue.Queue()
        self.queue_lock = threading.Lock()
        for i in self.taskdbmanager.GetData():
            self.q.put((i[0].encode('ascii','ignore'),i[1].encode('ascii','ignore'),i[2],i[3],i[4]))

    def DB(self):
        dbmanager = DBManager()
        while True:
            time.sleep(1)
            with self.qdb_lock:
                if not self.qdb.empty():
                    receipt = self.qdb.get()
                    dbmanager.StoreData(receipt)

    def Listen(self):
        t = threading.Thread(target = self.DB)
        t.daemon = True
        t.start()
        try:
            self.sock.listen(5)
            while True:
                client,address = self.sock.accept()
                #client.settimeout(300)
                t = threading.Thread(target = self.ListenToClient,args = (client,address))
                t.daemon = True
                t.start()
        except:
            L = []
            if not self.q.empty():
                for key in self.current:
                    L.append(self.current[key])
            while not self.q.empty():
                L.append(self.q.get())
            self.taskdbmanager.Clear()
            self.taskdbmanager.StoreAll(L)
            print "\n=====Task Saved====="

    def ListenToClient(self,client,address):
        size = 4096
        datemodify = 0
        print "Connect to {}".format(address)
        while True:
            with self.queue_lock:
                if self.q.empty():
                    break
            try:
                #job 0 number 1 date 2 direction 3 shift 4 distance
                with self.queue_lock:
                    job = self.q.get()
                with self.current_lock:
                    self.current[address] = job
                print "Assign Task : {} {} {} {} {}".format(job[0],job[1],job[2],job[3],job[4])
                client.sendall("{} {} {} {} {}".format(job[0],job[1],job[2],job[3],job[4]))
                data = client.recv(size)
                if data:
                    try:
                        receipt = json.loads(data)
                    except:
                        print data
                        raise Exception('Wrong Format')
                    with self.qdb_lock:
                        self.qdb.put(receipt)
                    datemodify = 0
                    if receipt.get(job[0][0:2]+str(int(job[0][2:])+job[3]+job[4]-1),job[1])[0] != job[1]:
                        datemodify = job[2]
                    if len(receipt) >= job[4]-5:
                        print "=====Add New Task====="
                        with self.queue_lock:
                            self.q.put((job[0],TimeConvert(job[1],datemodify),job[2],job[3]+job[4],job[4]))
                    else:
                        print "=====Search Reach The End====="          
                else:
                    print "no data"
                    raise Exception('Client Disconnected')
            except:
                client.close()
                print "Client Disconnected"
                break
        #with self.current_lock:
            #with self.queue_lock:
                #self.q.put(self.current[address])
    
if __name__ == '__main__':
    #log.basicConfig(level = log.DEBUG)
    T = TaskManager()
    T.Listen()
