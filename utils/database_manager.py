import sqlite3
from datetime import date

DATABASE = "database/attendance.db"


def get_connection():
    return sqlite3.connect(DATABASE)


def add_student(name, roll_number):
    """
    Adds a student to the database.
    """

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO students(name, roll_number)
            VALUES (?, ?)
            """,
            (name, roll_number)
        )

        connection.commit()
        print("✅ Student added to database.")

    except sqlite3.IntegrityError:
        print("⚠ Student already exists.")

    finally:
        connection.close()
def get_student_id(name, roll_number):
    """
    Returns the student ID if found.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id
        FROM students
        WHERE name = ? AND roll_number = ?
        """,
        (name, roll_number)
    )

    result = cursor.fetchone()

    connection.close()

    if result:
        return result[0]

    return None
from datetime import datetime


def mark_attendance(student_id):
    """
    Marks attendance only once per day.
    """

    connection = get_connection()
    cursor = connection.cursor()

    today = datetime.now().strftime("%Y-%m-%d")
    current_time = datetime.now().strftime("%H:%M:%S")

    # Check if attendance already exists
    cursor.execute(
        """
        SELECT *
        FROM attendance
        WHERE student_id = ? AND date = ?
        """,
        (student_id, today)
    )

    existing = cursor.fetchone()

    if existing:
        connection.close()
        return False, "Already Marked Today"

    # Insert new attendance
    cursor.execute(
        """
        INSERT INTO attendance(student_id, date, time)
        VALUES (?, ?, ?)
        """,
        (student_id, today, current_time)
    )

    connection.commit()
    connection.close()

    return True, "Attendance Marked"
def student_exists(roll_number):
    """
    Returns True if a student with this roll number already exists.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id
        FROM students
        WHERE roll_number = ?
        """,
        (roll_number,)
    )

    result = cursor.fetchone()

    connection.close()

    return result is not None

def get_total_students():
    """
    Returns total number of registered students.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM students")

    total = cursor.fetchone()[0]

    connection.close()

    return total

def get_today_attendance():
    """
    Returns today's attendance count.
    """

    connection = get_connection()
    cursor = connection.cursor()

    today = date.today().isoformat()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM attendance
        WHERE date = ?
        """,
        (today,)
    )

    total = cursor.fetchone()[0]

    connection.close()

    return total

def add_student(name, roll_number):
    """
    Adds a new student to the database.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO students(name, roll_number)
        VALUES(?, ?)
        """,
        (name, roll_number)
    )

    connection.commit()
    connection.close()

def get_all_students():
    """
    Returns all registered students.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, name, roll_number
        FROM students
        ORDER BY roll_number
    """)

    students = cursor.fetchall()

    connection.close()

    return students


def get_today_attendance_records():
    """
    Returns today's attendance records.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            students.roll_number,
            students.name,
            attendance.time
        FROM attendance
        JOIN students
        ON attendance.student_id = students.id
        WHERE attendance.date = DATE('now')
        ORDER BY students.roll_number
    """)

    records = cursor.fetchall()

    connection.close()

    return records

def search_students(keyword):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, name, roll_number
        FROM students
        WHERE
            name LIKE ?
            OR roll_number LIKE ?
        ORDER BY roll_number
    """, (f"%{keyword}%", f"%{keyword}%"))

    students = cursor.fetchall()

    connection.close()

    return students

def delete_student(student_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM attendance WHERE student_id=?",
        (student_id,)
    )

    cursor.execute(
        "SELECT name, roll_number FROM students WHERE id=?",
        (student_id,)
    )

    student = cursor.fetchone()

    cursor.execute(
        "DELETE FROM students WHERE id=?",
        (student_id,)
    )

    connection.commit()
    connection.close()

    return student
def update_student(student_id, new_name, new_roll):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            UPDATE students
            SET
                name=?,
                roll_number=?
            WHERE id=?
            """,
            (new_name, new_roll, student_id)
        )

        connection.commit()

        return True

    except sqlite3.IntegrityError:

        return False

    finally:

        connection.close()

def get_attendance_by_date(selected_date):
    """
    Returns attendance records for a given date.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            students.roll_number,
            students.name,
            attendance.time
        FROM attendance
        JOIN students
        ON attendance.student_id = students.id
        WHERE attendance.date = ?
        ORDER BY students.roll_number
    """, (selected_date,))

    records = cursor.fetchall()

    connection.close()

    return records

def get_statistics_by_date(selected_date):
    """
    Returns total students, present students,
    absent students and attendance percentage.
    """

    connection = get_connection()
    cursor = connection.cursor()

    # Total Students
    cursor.execute("""
        SELECT COUNT(*)
        FROM students
    """)

    total_students = cursor.fetchone()[0]

    # Present Students
    cursor.execute("""
        SELECT COUNT(*)
        FROM attendance
        WHERE date = ?
    """, (selected_date,))

    present_students = cursor.fetchone()[0]

    absent_students = total_students - present_students

    if total_students == 0:
        percentage = 0
    else:
        percentage = round(
            (present_students / total_students) * 100,
            2
        )

    connection.close()

    return (
        total_students,
        present_students,
        absent_students,
        percentage
    )