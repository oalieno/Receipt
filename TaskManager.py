import socket
import json
import logging as log

class TaskManager(object):

    def __init(self):
        self.receipt = {}

    def AssignTask(self,number,date,distance):
        server = ('localhost',5555)
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.connect(server)
        try:
            sock.sendall("{} {} {}".format(number,date,str(distance)))
            self.receipt = json.loads(sock.recv(4096))
            sock.close()
            log.debug(self.receipt)
        except socket.error as e:
            sock.close()
            print "shit happened {}".format(e)    

if __name__ == '__main__':
    T = TaskManager()
    T.AssignTask("HB22675221","105/05/15",10)
