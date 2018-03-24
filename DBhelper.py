import sqlite3


class DBHelper:

    primary_key = 1

    def __init__(self, dbname="todo.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)

    def setup(self):
        stmt = "CREATE TABLE IF NOT EXISTS rhymes (words text, phonemes text)"
        self.conn.execute(stmt)
        self.conn.commit()

        # for start and debug reasons, drop the rhymes table before every start:
        # stmt = "DELETE FROM rhymes"
        # self.conn.execute(stmt)
        # self.conn.commit()

        stmt = "SELECT words FROM rhymes"
        result = self.conn.execute(stmt)
        if result.fetchone() is None:
            print("Create rhyme DB")
            stmt = "CREATE TABLE IF NOT EXISTS rhymes (words text, phonemes text)"
            self.conn.execute(stmt)
            self.conn.commit()

            raw_data = open("dictionary.txt", 'r').readlines()
            data = []
            for line in raw_data:
                line = line.replace("\n", "")
                word = ""
                for i, c in enumerate(line):
                    if c == " " and line[i+1] == " ":
                        continue
                    elif c == " ":
                        word += ";"
                    else:
                        word += c
                words = word.split(";")
                ph = " ".join(words[2:])
                data.append([words[0], ph])

            stmt = "INSERT INTO rhymes (words, phonemes) VALUES (?, ?)"
            for line in data:
                args = (line[0], line[1],)
                self.conn.execute(stmt, args)
            self.conn.commit()

        else:
            print("DB already exists")

        # start building kanye db:
        # stmt = "DELETE FROM kanye"
        # self.conn.execute(stmt)
        # self.conn.commit()

        stmt = "SELECT word FROM kanye"
        result = self.conn.execute(stmt)
        if result.fetchone() is None:
            print("Create kanye DB")
            stmt = "CREATE TABLE IF NOT EXISTS kanye (row integer, word text)"
            self.conn.execute(stmt)
            self.conn.commit()

            raw_data = open("KanyeWest.txt", 'r', encoding='UTF-8').readlines()
            data = []
            for index, line in enumerate(raw_data):
                line = line.replace("\n", "")
                word = line.split(" ")[-1]
                stmt = "INSERT INTO kanye (row, word) VALUES (?, ?)"
                args = (index, word,)
                self.conn.execute(stmt, args)
            self.conn.commit()
        else:
            print("DB kanye already exists")
        print("finish setting up DB")


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

    def get_items(self, table):
        if table == "rhymes":
            stmt = "SELECT words, phonemes FROM " + table
        elif table == "kanye":
            stmt = "SELECT row, word FROM " + table
        table = [[x, y] for x, y in self.conn.execute(stmt)]
        words = [x[0] for x in table]
        phonemes = [y[1] for y in table]
        return words, phonemes

    def get_index(self, table, word):
        if table == "rhymes":
            print("use another function")
        else:
            stmt = "SELECT row FROM " + table + " WHERE word = (?)"
            args = (word, )
            result = self.conn.execute(stmt, args)
            return result.fetchone()
