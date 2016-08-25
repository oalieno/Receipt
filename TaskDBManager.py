import sqlite3
import sys

class TaskDBManager(object):
    def __init__(self):
	self.conn = sqlite3.connect("DB/task.db")
	self.c = self.conn.cursor()

    def CreateTable(self):
	self.c.execute("CREATE TABLE if not exists task (id TEXT,date TEXT,direction INTEGER,shift INTEGER,distance INTEGER)")

    def StoreAll(self,data):
	for i in data:
	    self.c.execute("SELECT * FROM task WHERE id == '{}' AND date == '{}' AND direction == {} AND shift == {} AND distance == {}".format(i[0],i[1],i[2],i[3],i[4]))
	    if self.c.fetchone() == None:
		self.c.execute("INSERT INTO task VALUES ('{}','{}',{},{},{})".format(i[0],i[1],i[2],i[3],i[4]))
	self.conn.commit()

    def GetData(self):
	self.c.execute("SELECT * FROM task") 
	return self.c.fetchall()
    
    def Clear(self):
	self.c.execute("DELETE FROM task")
	self.conn.commit()

if __name__ == '__main__':
    D = TaskDBManager()
    try:
	if len(sys.argv) < 2:
	    print 'USAGE : '
	    print '-create                                 Create Table'
	    print '-clear                                  Clear Table'
	    print '-show -num                              Show How many data in Table'
	    print '-show -all                              Show Table'
	    print '-add [id] [date] (optional:[direction]) Add new Task'
	elif sys.argv[1][1:] == 'create':
	    D.CreateTable()
	elif sys.argv[1][1:] == 'clear':
	    option = raw_input("Are you sure?")
	    if option == 'y':
	        D.Clear()
	elif sys.argv[1][1:] == 'show':
	    if sys.argv[2][1:] == 'num':
	        D.c.execute("SELECT COUNT(*) FROM receipt")
	        print "=====Total: "+repr(D.c.fetchone()[0])+"====="
	    elif sys.argv[2][1:] == 'all':
	        D.c.execute("SELECT * FROM task ORDER BY id Asc")
	        result = D.c.fetchall()
	        print "id\t\tdate\t\tdirection\tshift\tdistance"
	        for i in result:
		    print i[0].encode("utf-8")+'\t'+i[1].encode("utf-8")+'\t'+str(i[2])+'\t\t'+str(i[3])+'\t'+str(i[4])
	    else:
	        raise error
	elif sys.argv[1][1:] == 'add':
	    if len(sys.argv[2]) != 10 or len(sys.argv[3]) != 9 or sys.argv[3][3] != '/' or sys.argv[3][6] != '/':
	        raise Exception("wrong id or date format")
	    if len(sys.argv) == 5:
	        if int(sys.argv[4]) != 1 and int(sys.argv[4]) != -1:
		    raise Exception("wrong direction")
	        D.StoreAll([(sys.argv[2],sys.argv[3],int(sys.argv[4]),0,10)])
	    else:
	        D.StoreAll([(sys.argv[2],sys.argv[3],1,0,10),(sys.argv[2],sys.argv[3],-1,0,10)])
	else:
	    raise Exception("parameter error")
    except Exception as e:
	print e
		 
