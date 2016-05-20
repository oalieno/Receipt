import sqlite3

class DBManager(object):
    def __init__(self):
        self.conn = sqlite3.connect("receipt.db")
        self.c = self.conn.cursor()
    def CreateTable(self):
        self.c.execute("CREATE TABLE if not exists receipt (id TEXT, date TEXT, money INTEGER)")
    def StoreData(self,table,data):
        for key in data: 
            self.c.execute("SELECT * FROM {} WHERE id == '{}'".format(table,key))
            if self.c.fetchone() == None:
                self.c.execute("INSERT INTO {} VALUES ('{}','{}',{})".format(table,key,receipt[key][0],receipt[key][1]))
        self.conn.commit()

if __name__ == '__main__':
    D = DBManager()
    D.c.execute("SELECT * FROM receipt")
    print D.c.fetchall()
