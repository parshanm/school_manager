import sqlite3


class DataBase:
    def __init__(self):
        self.connection = sqlite3.connect("database.db")
        self.cursor = self.connection.cursor()

    def create_tables(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS students (
                id TEXT PRIMARY KEY,
                name TEXT,
                grade TEXT,
                checkin_date TEXT,
                status TEXT,
                parent_phone TEXT,
                student_phone TEXT
            );
        """
        )
        self.connection.commit()
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS teachers (
                id TEXT PRIMARY KEY,
                name TEXT,
                lesson TEXT
            );
        """
        )
        self.connection.commit()

    def read_students(self):
        res = self.cursor.execute("""SELECT * FROM students""").fetchall()
        return res

    def read_teachers(self):
        res = self.cursor.execute("""SELECT * FROM teachers""").fetchall()
        return res

    def write_students(
        self, id, name, grade, checkin_date, status, parent_phone, student_phone
    ):
        self.cursor.execute(
            """
            INSERT INTO students (id, name, grade, checkin_date, status, parent_phone, student_phone)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
            (id, name, grade, checkin_date, status, parent_phone, student_phone),
        )
        self.connection.commit()

    def write_teachers(self, id, name, lesson):
        self.cursor.execute(
            """
            INSERT INTO teachers (id, name, lesson)
            VALUES (?, ?, ?)
        """,
            (id, name, lesson),
        )
        self.connection.commit()

    def get_student_count(self):
        res = self.cursor.execute("""SELECT COUNT(*) FROM students""").fetchone()
        return str(res[0])

    def get_teachers_count(self):
        res = self.cursor.execute("""SELECT COUNT(*) FROM teachers""").fetchone()
        return str(res[0])

    def delete_student(self, id):
        self.cursor.execute(
            """
            DELETE FROM students WHERE id = ?
        """,
            (id,),
        )
        self.connection.commit()

    def delete_teacher(self, id):
        self.cursor.execute(
            """
            DELETE FROM teachers WHERE id = ?
        """,
            (id,),
        )
        self.connection.commit()

    def add_classes(self, lesson, teacher, start, end, name):
        query = """
            CREATE TABLE IF NOT EXISTS classes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                lesson TEXT,
                teacher TEXT,
                start TEXT,
                end TEXT,
                name TEXT
            );
        """
        self.cursor.execute(query)
        self.connection.commit()

        query_1 = """
            INSERT INTO classes (lesson, teacher, start, end, name)
            VALUES (?, ?, ?, ?, ?)
        """
        self.cursor.execute(query_1, (lesson, teacher, start, end, name))
        self.connection.commit()

    def delete_class(self, id):
        self.cursor.execute(
            """
            DELETE FROM classes WHERE id = ?
        """,
            (id,),
        )

    def read_classes(self):
        res = self.cursor.execute("""SELECT * FROM classes""").fetchall()
        return res

    def get_classes_count(self):
        res = self.cursor.execute("""SELECT COUNT(*) FROM classes""").fetchone()
        return str(res[0])

    def search_student(self, filter, data):
        query = f"""SELECT * FROM students WHERE {filter}=?"""
        res = self.cursor.execute(query, (data,)).fetchall()
        print(res)
        return res


if __name__ == "__main__":
    pass
    # db = DataBase()
    # db.create_tables()
    # r = db.read_students()
    # print(r)
    # db.write_students('1', 'John Doe', '10', '2023-10-01', 'فعال', '1234567890')
    # db.write_teachers('1', 'Jane Smith', 'Math')
    # r = db.read_teachers()
    # print(r)
    # r = db.get_student_count()
    # print(r)
    # r = db.get_teachers_count()
    # print(r)
    # db.delete_student('1')
    # db.delete_teacher('1')
    # db.add_classes('math', 'Jane Smith', '9:30', '11:00', '902')
    # r = db.read_classes()
    # print(r)
    # r = db.search_student('name', 'parshan mazaheri')
    # print(r)