import sqlite3
import hashlib
import shutil
import os
from datetime import datetime

DB_NAME = "students.db"


# ---------------------------
# CONNECTION
# ---------------------------
def connect():
    return sqlite3.connect(DB_NAME)


# ---------------------------
# PASSWORD ENCRYPTION
# ---------------------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# ---------------------------
# CREATE ALL TABLES
# ---------------------------
def create_tables():
    conn = connect()
    cur = conn.cursor()

    # Students Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER,
        course TEXT,
        email TEXT
    )
    """)

    # Users Table (Login System)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    # Attendance Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        date TEXT,
        status TEXT
    )
    """)

    # Export Logs Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS export_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        file_name TEXT,
        export_date TEXT
    )
    """)

    # Default Admin
    cur.execute("SELECT * FROM users WHERE username='admin'")
    if not cur.fetchone():
        cur.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            ("admin", hash_password("admin"))
        )

    conn.commit()
    conn.close()


# ---------------------------
# ADD USER (with encryption)
# ---------------------------
def add_user(username, password):
    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, hash_password(password))
        )
        conn.commit()
        print("User created")
    except:
        print("User already exists")

    conn.close()


# ---------------------------
# VERIFY LOGIN
# ---------------------------
def verify_user(username, password):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, hash_password(password))
    )

    result = cur.fetchone()
    conn.close()
    return result


# ---------------------------
# ATTENDANCE MARK
# ---------------------------
def mark_attendance(student_id, status):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO attendance (student_id, date, status) VALUES (?, ?, ?)",
        (student_id, datetime.now().strftime("%Y-%m-%d"), status)
    )

    conn.commit()
    conn.close()


# ---------------------------
# EXPORT LOG
# ---------------------------
def log_export(file_name):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO export_logs (file_name, export_date) VALUES (?, ?)",
        (file_name, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )

    conn.commit()
    conn.close()


# ---------------------------
# DATABASE BACKUP
# ---------------------------
def backup_database():
    if not os.path.exists(DB_NAME):
        print("Database not found")
        return

    backup_name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
    shutil.copy(DB_NAME, backup_name)

    print(f"Backup created: {backup_name}")


# ---------------------------
# INIT
# ---------------------------
create_tables()