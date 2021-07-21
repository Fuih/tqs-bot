import sqlite3

DATABASE = "bot/db/tqs.db"

class Champ:

    fields = ["id", "name", "cn_name", "faction", "reworked", "original_desc", "new_desc", "hp", "banned"]

    def get_all_champs(self):
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        query = "select * from champs where name not null"
        cursor.execute(query)
        result = cursor.fetchall()
        result = [dict(zip(self.fields, r)) for r in result]

        conn.close()        

        return result

    def get_champ_by_name(self, name):
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        query = "select * from champs where name = ? or cn_name = ?"
        cursor.execute(query, (name, name))
        result = cursor.fetchone()
        
        if result != None:
            result = dict(zip(self.fields, result))
        
        conn.close()        

        return result

    def get_champ_by_cn_name(self, name):
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        query = "select * from champs where cn_name = ?"
        cursor.execute(query, (name,))
        result = cursor.fetchone()
        
        if result != None:
            result = dict(zip(self.fields, result))

        conn.close()        

        return result


# conn = sqlite3.connect(DATABASE)
# cursor = conn.cursor()
# import os
# filepath = "D:/Project/VSCode/TQS-Bot/src/db/cards"
# cards = os.listdir(filepath)
# cards = ['("{}")'.format(c) for c in cards]
# cards = ",".join(cards).replace(".jpg","")
# query = "insert into cards(cn_name) values {};".format(cards)

# cursor.execute(query)
# conn.commit()



