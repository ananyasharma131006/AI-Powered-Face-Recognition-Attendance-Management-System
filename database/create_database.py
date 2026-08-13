import sqlite3
from pathlib import Path

# Create database folder if it doesn't exist
Path("database").mkdir(exist_ok=True)

# Connect to database
connection = sqlite3.connect("database/attendance.db")

cursor = connection.cursor()

# --------------------------
# Students Table
# --------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    name TEXT NOT NULL,

    roll_number TEXT UNIQUE NOT NULL
)
""")

# --------------------------
# Attendance Table
# --------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS attendance (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    student_id INTEGER,

    date TEXT,

    time TEXT,

    FOREIGN KEY(student_id)
        REFERENCES students(id)

)
""")

connection.commit()

connection.close()

print("Database Created Successfully!")