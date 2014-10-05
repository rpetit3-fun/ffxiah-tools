'''

'''
import pymysql

class DSPDB(object):

    def __init__(self):
        self.items = {}
    
    def __connect(self):
        self.conn = pymysql.connect(host='localhost', port=3306, user='dspdb', 
                                    passwd='dspdb', db='dspdb')
    
    def __disconnect(self):
        self.conn.close()
        
    def dsp_items(self):
        self.__connect()
        cur = self.conn.cursor()
        cur.execute("SELECT itemid, name, stackSize, aH FROM item_basic")
        for row in cur.fetchall():
            self.items[str(row[0])] = {
                'name':row[1],
                'stack':row[2],
                'category':str(row[3])
            }
        cur.close()
        self.__disconnect()
        
    def update_category(self, item_id, category):
        sql = "UPDATE item_basic SET aH={0} WHERE itemid={1}".format(category, 
                                                                     item_id)
        self.__connect()
        cur = self.conn.cursor()
        cur.execute(sql)
        cur.fetchall()
        cur.close()
        self.__disconnect()