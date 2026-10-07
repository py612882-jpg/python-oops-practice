import sqlite3


class Database:
    def __init__(self, db_name="student_management.db"):
        self.db_name = db_name
        self.create_tables()

    def connect(self):
        connection = sqlite3.connect(self.db_name)

        # Enable foreign key support in SQLite
        connection.execute("PRAGMA foreign_keys = ON")

        return connection

    # -------------------------
    # CREATE TABLES
    # -------------------------

    def create_tables(self):

        connection = self.connect()
        cursor = connection.cursor()

        # Courses table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS courses (
                course_id INTEGER PRIMARY KEY,
                course_name TEXT NOT NULL UNIQUE
            )
        """)

        # Students table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                student_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                age INTEGER NOT NULL CHECK(age > 0),
                course_id INTEGER NOT NULL,
                marks REAL NOT NULL CHECK(marks >= 0 AND marks <= 100),
                FOREIGN KEY (course_id)
                    REFERENCES courses(course_id)
            )
        """)

        connection.commit()
        connection.close()

    # -------------------------
    # COURSE METHODS
    # -------------------------

    def add_course(self, course):
        connection = self.connect()
        cursor = connection.cursor()

        try:
            course.validate()

            cursor.execute("""
                INSERT INTO courses (course_id, course_name)
                VALUES (?, ?)
            """, (course.course_id, course.course_name))

            connection.commit()
            return True

        except sqlite3.IntegrityError as error:
            print("Error:", error)
            return False

        finally:
            connection.close()

    def get_all_courses(self):
        connection = self.connect()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT course_id, course_name
            FROM courses
            ORDER BY course_id
        """)

        courses = cursor.fetchall()
        connection.close()

        return courses

    def get_course_by_id(self, course_id):
        connection = self.connect()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT course_id, course_name
            FROM courses
            WHERE course_id = ?
        """, (course_id,))

        course = cursor.fetchone()
        connection.close()

        return course

    def delete_course(self, course_id):
        connection = self.connect()
        cursor = connection.cursor()

        try:
            cursor.execute("""
                DELETE FROM courses
                WHERE course_id = ?
            """, (course_id,))

            connection.commit()

            return cursor.rowcount > 0

        except sqlite3.IntegrityError:
            print("Cannot delete course because students are using it.")
            return False

        finally:
            connection.close()

    # -------------------------
    # STUDENT METHODS
    # -------------------------

    def add_student(self, student):
        connection = self.connect()
        cursor = connection.cursor()

        try:
            student.validate()

            # Check whether course exists
            cursor.execute("""
                SELECT course_id
                FROM courses
                WHERE course_id = ?
            """, (student.course_id,))

            course = cursor.fetchone()

            if course is None:
                print("Invalid course ID.")
                return False

            cursor.execute("""
                INSERT INTO students
                (student_id, name, age, course_id, marks)
                VALUES (?, ?, ?, ?, ?)
            """, (
                student.student_id,
                student.name,
                student.age,
                student.course_id,
                student.marks
            ))

            connection.commit()
            return True

        except sqlite3.IntegrityError as error:
            print("Error:", error)
            return False

        finally:
            connection.close()

    def get_all_students(self):
        connection = self.connect()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                student_id,
                name,
                age,
                course_id,
                marks
            FROM students
            ORDER BY student_id
        """)

        students = cursor.fetchall()
        connection.close()

        return students

    def get_student_by_id(self, student_id):
        connection = self.connect()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                student_id,
                name,
                age,
                course_id,
                marks
            FROM students
            WHERE student_id = ?
        """, (student_id,))

        student = cursor.fetchone()
        connection.close()

        return student

    def update_student(self, student_id, name, age, course_id, marks):
        connection = self.connect()
        cursor = connection.cursor()

        try:
            # Check course
            cursor.execute("""
                SELECT course_id
                FROM courses
                WHERE course_id = ?
            """, (course_id,))

            if cursor.fetchone() is None:
                print("Invalid course ID.")
                return False

            cursor.execute("""
                UPDATE students
                SET name = ?,
                    age = ?,
                    course_id = ?,
                    marks = ?
                WHERE student_id = ?
            """, (name, age, course_id, marks, student_id))

            connection.commit()

            return cursor.rowcount > 0

        except sqlite3.IntegrityError as error:
            print("Error:", error)
            return False

        finally:
            connection.close()

    def delete_student(self, student_id):
        connection = self.connect()
        cursor = connection.cursor()

        cursor.execute("""
            DELETE FROM students
            WHERE student_id = ?
        """, (student_id,))

        connection.commit()

        deleted = cursor.rowcount > 0

        connection.close()

        return deleted

    # -------------------------
    # JOIN METHODS
    # -------------------------

    def get_students_with_courses(self):
        connection = self.connect()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                s.student_id,
                s.name,
                c.course_name,
                s.marks
            FROM students AS s
            INNER JOIN courses AS c
                ON s.course_id = c.course_id
        """)

        results = cursor.fetchall()
        connection.close()

        return results

    def get_students_by_course(self, course_name):
        connection = self.connect()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                s.name,
                c.course_name,
                s.marks
            FROM students AS s
            INNER JOIN courses AS c
                ON s.course_id = c.course_id
            WHERE c.course_name = ?
        """, (course_name,))

        results = cursor.fetchall()
        connection.close()

        return results

    def get_course_statistics(self):
        connection = self.connect()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                c.course_name,
                COUNT(s.student_id) AS total_students,
                AVG(s.marks) AS average_marks,
                MAX(s.marks) AS highest_marks,
                MIN(s.marks) AS lowest_marks
            FROM courses AS c
            LEFT JOIN students AS s
                ON c.course_id = s.course_id
            GROUP BY c.course_id, c.course_name
        """)

        results = cursor.fetchall()
        connection.close()

        return results

    def get_courses_without_students(self):
        connection = self.connect()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT c.course_name
            FROM courses AS c
            LEFT JOIN students AS s
                ON c.course_id = s.course_id
            WHERE s.student_id IS NULL
        """)

        results = cursor.fetchall()
        connection.close()

        return results

    # -------------------------
    # STUDENT SEARCH / SORT
    # -------------------------

    def search_students_by_marks(self, min_marks):
        connection = self.connect()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                student_id,
                name,
                age,
                course_id,
                marks
            FROM students
            WHERE marks >= ?
            ORDER BY marks DESC
        """, (min_marks,))

        results = cursor.fetchall()
        connection.close()

        return results

    def sort_students(self, column):
        allowed_columns = {
            "name": "name",
            "marks": "marks",
            "age": "age"
        }

        if column not in allowed_columns:
            return []

        connection = self.connect()
        cursor = connection.cursor()

        query = f"""
            SELECT
                student_id,
                name,
                age,
                course_id,
                marks
            FROM students
            ORDER BY {allowed_columns[column]}
        """

        cursor.execute(query)

        results = cursor.fetchall()
        connection.close()

        return results

    def top_n_students(self, n):
        connection = self.connect()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                student_id,
                name,
                age,
                course_id,
                marks
            FROM students
            ORDER BY marks DESC
            LIMIT ?
        """, (n,))

        results = cursor.fetchall()
        connection.close()

        return results

    def student_statistics(self):
        connection = self.connect()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                COUNT(*),
                AVG(marks),
                MAX(marks),
                MIN(marks)
            FROM students
        """)

        result = cursor.fetchone()
        connection.close()

        return result