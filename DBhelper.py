import sqlite3


class DBHelper:

    primary_key = 1

    def __init__(self, dbname="todo.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)

    def setup(self):
        # stmt = "DROP TABLE items2"
        # self.conn.execute(stmt)
        # self.conn.commit()
        stmt = "CREATE TABLE IF NOT EXISTS items2 (id integer, description text)"
        self.conn.execute(stmt)
        self.conn.commit()

    def add_item(self, item_text):
        stmt = "INSERT INTO items2 (id, description) VALUES (?, ?)"
        args = (self.primary_key, item_text, )
        self.conn.execute(stmt, args)
        self.conn.commit()
        self.primary_key += 1

    def delete_item(self, item_text):
        stmt = "DELETE FROM items2 WHERE description = (?)"
        args = (item_text, )
        self.conn.execute(stmt, args)
        self.conn.commit()

    def get_items(self):
        stmt = "SELECT id, description FROM items2"
        table = [[x, y] for x, y in self.conn.execute(stmt)]
        ids = [x[0] for x in table]
        texts = [y[1] for y in table]
        return ids, texts