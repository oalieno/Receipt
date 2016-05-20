import sqlite3

class ImgDBManager(object):
    def __init__(self):
        self.conn = sqlite3.connect("image.db")
        self.c = self.conn.cursor()
    def CreateTable(self):
        self.c.execute("CREATE TABLE if not exists image (id TEXT, captcha)")
    def StoreData(self,SHA,captcha):
        self.c.execute("SELECT * FROM image WHERE id == '{}'".format(SHA))
        if self.c.fetchone() == None:
            self.c.execute("INSERT INTO image VALUES ('{}','{}')".format(SHA,captcha))
        self.conn.commit()
    def SearchID(self,SHA):
        self.c.execute("SELECT * FROM image WHERE id == '{}'".format(SHA))
        return self.c.fetchone()

if __name__ == '__main__':
    D = ImgDBManager()
    D.CreateTable()
