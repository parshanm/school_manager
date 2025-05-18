import sqlite3

class DataBase:
    def __init__(self):
        self.connection = sqlite3.connect('database.db')
        self.cursor = self.connection.cursor()
    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id TEXT PRIMARY KEY,
                name TEXT,
                grade TEXT,
                checkin_date TEXT,
                status TEXT
            );
        ''')
        self.connection.commit()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS teachers (
                id TEXT PRIMARY KEY,
                name TEXT,
                lesson TEXT
            );
        ''')
        self.connection.commit()

    def read_students(self):
        res = self.cursor.execute('''SELECT * FROM students''').fetchall()
        return res

if __name__ == '__main__':
    db = DataBase()
    # db.create_tables()
    r = db.read_students()
    print(r)
