import sqlite3

class SQLHandler(object):
    def __init__(self, path):
        self.db = sqlite3.connect(path)
        self.cursor = self.db.cursor()

    def execute(self, sql):
         try:
            # print(sql)
            self.cursor.execute(sql)
            self.db.commit()
         except sqlite3.IntegrityError:
            pass

    def execute_return(self, sql):
        ret = self.cursor.execute(sql)
        return ret

    def insert_binary(self, sql, bin_obj, ):
        # print(sql)
        self.cursor.execute(sql, (bin_obj, ))
        self.db.commit()

    def close(self):
        self.db.close()