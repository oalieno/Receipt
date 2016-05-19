import sqlite3

class DBManager(object):
    def __init__(self):
        self.conn = sqlite3.connect("receipt.db")
        self.c = self.conn.cursor()
    def CreateTable(self):
        self.c.execute("CREATE TABLE receipt (id TEXT, date TEXT, money INTEGER)")
    def StoreData(self,receipt):
        for key in receipt: 
            self.c.execute("SELECT * FROM receipt WHERE id == '{}'".format(key))
            if self.c.fetchone() == None:
                self.c.execute("INSERT INTO receipt VALUES ('{}','{}',{})".format(key,receipt[key][0],receipt[key][1]))
        self.conn.commit()

if __name__ == '__main__':
    D = DBManager()
    D.c.execute("SELECT * FROM receipt")
    print D.c.fetchall()
