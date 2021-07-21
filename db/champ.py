class Champ:

    fields = ["id", "name", "cn_name", "faction", "reworked", "original_desc", "new_desc", "hp", "banned"]

    def __init__(self, conn):
        self.conn = conn

    def get_all_champs(self):
        cursor = self.conn.cursor()

        query = "select * from champs where name not null"
        cursor.execute(query)
        result = cursor.fetchall()
        result = [dict(zip(self.fields, r)) for r in result] 

        return result

    def get_champ_by_name(self, name):
        cursor = self.conn.cursor()

        query = "select * from champs where name = ? or cn_name = ?"
        cursor.execute(query, (name, name))
        result = cursor.fetchone()
        
        if result != None:
            result = dict(zip(self.fields, result))      

        return result

    def get_champ_by_cn_name(self, name):
        cursor = self.conn.cursor()

        query = "select * from champs where cn_name = ?"
        cursor.execute(query, (name,))
        result = cursor.fetchone()
        
        if result != None:
            result = dict(zip(self.fields, result))    

        return result


