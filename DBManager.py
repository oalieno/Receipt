import sqlite3
import sys

class DBManager(object):
    def __init__(self):
        self.conn = sqlite3.connect("DB/receipt.db")
        self.c = self.conn.cursor()
    def CreateTable(self):
        self.c.execute("CREATE TABLE if not exists receipt (id TEXT, date TEXT, money INTEGER)")
    def StoreData(self,data):
        for key in data: 
            self.c.execute("SELECT * FROM receipt WHERE id == '{}'".format(key))
            if self.c.fetchone() == None:
                self.c.execute("INSERT INTO receipt VALUES ('{}','{}',{})".format(key,data[key][0],data[key][1]))
        self.conn.commit()

if __name__ == '__main__':
    D = DBManager()
    if len(sys.argv) < 2:
        print 'USAGE :'
        print '-create        Create Table'
        print '-show -num     Show How many data in Table'
        print '-show -all     Show All Data'
    elif sys.argv[1][1:] == 'create':
        D.CreateTable()
    elif sys.argv[1][1:] == 'show':
        if sys.argv[2][1:] == 'num':
            D.c.execute("SELECT COUNT(*) FROM receipt")
            print "=====Total : ",D.c.fetchone(),"====="
        elif sys.argv[2][1:] == 'all':
            D.c.execute("SELECT * FROM receipt ORDER BY id Asc")
            print D.c.fetchall()
	else:
 	    print 'wrong parameter!!'
    else:
        print 'wrong parameter!!'
