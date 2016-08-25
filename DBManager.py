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
            print "=====Total : "+repr(D.c.fetchone()[0])+"====="
        elif sys.argv[2][1:] == 'all':
            D.c.execute("SELECT * FROM receipt ORDER BY id Asc")
            result = D.c.fetchall()
	    print len(result)
	    print "id\t\tdate\t\tmoney"
	    for i in range(len(result)-1):
                print result[i][0]+'\t'+result[i][1]+'\t'+str(result[i][2])
		if(int(result[i][0][2:])-int(result[i+1][0][2:]) > 1):
		    print "=====fault zone====="
            print result[len(result)-1][0]+'\t'+result[len(result)-1][1]+'\t'+str(result[len(result)-1][2])
	else:
 	    print 'wrong parameter!!'
    else:
        print 'wrong parameter!!'
