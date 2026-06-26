import sqlite3
import csv

def export_csv():
    conn = sqlite3.connect("students.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM students")
    rows = cur.fetchall()

    with open("students.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Name", "Age", "Course", "Email"])
        writer.writerows(rows)

    conn.close()
    print("Exported successfully")