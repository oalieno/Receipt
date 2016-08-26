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
	print '-show -id      Show the data with the specific id'
	print '-show -date    Show Data by date'
	print '-show -hole    Show the empty zone of the Data'
        print '-show -all     Show All Data'
    elif sys.argv[1][1:] == 'create':
        D.CreateTable()
    elif sys.argv[1][1:] == 'show':
        if sys.argv[2][1:] == 'num':
            D.c.execute("SELECT COUNT(*) FROM receipt")
            print "Total : "+repr(D.c.fetchone()[0])
        elif sys.argv[2][1:] == 'all':
            D.c.execute("SELECT * FROM receipt ORDER BY id Asc")
            result = D.c.fetchall()
	    print "Total : "+str(len(result))
	    print "id\t\tdate\t\tmoney"
	    for i in range(len(result)-1):
                print result[i][0]+'\t'+result[i][1]+'\t'+str(result[i][2])
		if(int(result[i][0][2:])-int(result[i+1][0][2:]) > 1):
		    print "=====fault zone====="
            print result[len(result)-1][0]+'\t'+result[len(result)-1][1]+'\t'+str(result[len(result)-1][2])
        elif sys.argv[2][1:] == 'id':
	    D.c.execute("SELECT * FROM receipt WHERE id == '{}'".format(sys.argv[3]))
	    result = D.c.fetchone()
	    print "id\t\tdate\t\tmoney"
	    print result[0]+'\t'+result[1]+'\t'+str(result[2])
	elif sys.argv[2][1:] == 'date':
            D.c.execute("SELECT * FROM receipt ORDER BY date Asc")
            result = D.c.fetchall()
	    print "date"+'\t\t'+"count"+'\t'+"total"
	    now = ""
	    count = 0
	    total = 0
	    for i in range(len(result)):
	    	if now != result[i][1]:
		    if now != "":
			print now+'\t'+str(count)+'\t'+str(total)
	 	    now = result[i][1]
		    count = 0
		    total = 0
		count += 1
		total += result[i][2]
	    print now+'\t'+str(count)+'\t'+str(total)
	elif sys.argv[2][1:] == 'hole':
            D.c.execute("SELECT * FROM receipt ORDER BY id Asc")
            result = D.c.fetchall()
	    print "start"+'\t\t'+"end"+'\t\t'+"gap"
	    for i in range(len(result)-1):
		gap = int(result[i+1][0][2:])-int(result[i][0][2:])-1
		if gap == 1:
		    print result[i][0][:2]+str(int(result[i][0][2:])+1)+'\t'+result[i][0][:2]+str(int(result[i][0][2:])+1)+'\t'+str(gap)
		elif gap > 1:  
		    print result[i][0][:2]+str(int(result[i][0][2:])+1)+'\t'+result[i+1][0][:2]+str(int(result[i+1][0][2:])-1)+'\t'+str(gap)
	else:
 	    print 'wrong parameter!!'
    else:
        print 'wrong parameter!!'
