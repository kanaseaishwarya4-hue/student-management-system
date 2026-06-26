import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from database import mark_attendance, backup_database
from export import export_csv

DB_NAME = "students.db"


# ---------------------------
# DB CONNECT
# ---------------------------
def connect():
    return sqlite3.connect(DB_NAME)


# ---------------------------
# LOAD DATA
# ---------------------------
def load_students():
    for row in tree.get_children():
        tree.delete(row)

    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM students")
    rows = cur.fetchall()
    conn.close()

    for row in rows:
        tree.insert("", tk.END, values=row)

    count_label.config(text=f"Total Students: {len(rows)}")


# ---------------------------
# ADD STUDENT
# ---------------------------
def add_student():
    if name.get() == "" or course.get() == "":
        messagebox.showerror("Error", "Fill required fields")
        return

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO students (name, age, course, email)
        VALUES (?, ?, ?, ?)
    """, (name.get(), age.get(), course.get(), email.get()))

    conn.commit()
    conn.close()

    load_students()


# ---------------------------
# DELETE STUDENT
# ---------------------------
def delete_student():
    selected = tree.focus()
    if not selected:
        messagebox.showerror("Error", "Select record")
        return

    data = tree.item(selected)["values"]

    conn = connect()
    cur = conn.cursor()

    cur.execute("DELETE FROM students WHERE id=?", (data[0],))
    conn.commit()
    conn.close()

    load_students()


# ---------------------------
# UPDATE STUDENT (NEW 🔥)
# ---------------------------
def update_student():
    selected = tree.focus()
    if not selected:
        messagebox.showerror("Error", "Select record")
        return

    data = tree.item(selected)["values"]

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        UPDATE students
        SET name=?, age=?, course=?, email=?
        WHERE id=?
    """, (
        name.get(),
        age.get(),
        course.get(),
        email.get(),
        data[0]
    ))

    conn.commit()
    conn.close()

    load_students()


# ---------------------------
# SEARCH STUDENT (NEW 🔥)
# ---------------------------
def search_student():
    query = search.get()

    for row in tree.get_children():
        tree.delete(row)

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT * FROM students
        WHERE name LIKE ? OR course LIKE ?
    """, (f"%{query}%", f"%{query}%"))

    rows = cur.fetchall()
    conn.close()

    for row in rows:
        tree.insert("", tk.END, values=row)

    count_label.config(text=f"Found: {len(rows)}")


# ---------------------------
# RESET
# ---------------------------
def reset_data():
    search.delete(0, tk.END)
    load_students()


# ---------------------------
# AUTO FILL (NEW 🔥)
# ---------------------------
def fill_data(event):
    selected = tree.focus()
    if not selected:
        return

    data = tree.item(selected)["values"]

    name.delete(0, tk.END)
    age.delete(0, tk.END)
    course.delete(0, tk.END)
    email.delete(0, tk.END)

    name.insert(0, data[1])
    age.insert(0, data[2])
    course.insert(0, data[3])
    email.insert(0, data[4])


# ---------------------------
# ATTENDANCE
# ---------------------------
def mark_present():
    selected = tree.focus()
    if not selected:
        return

    data = tree.item(selected)["values"]
    mark_attendance(data[0], "Present")
    messagebox.showinfo("Success", "Attendance marked")


# ---------------------------
# EXPORT
# ---------------------------
def export_data():
    export_csv()
    messagebox.showinfo("Export", "CSV Exported")


# ---------------------------
# BACKUP
# ---------------------------
def backup_db():
    backup_database()
    messagebox.showinfo("Backup", "Database backup created")


# ---------------------------
# DASHBOARD UI
# ---------------------------
def open_dashboard():
    global root, tree, name, age, course, email, count_label, search

    root = tk.Tk()
    root.title("Student Management System Pro")
    root.geometry("1100x650")
    root.configure(bg="#1e1e2f")

    # TITLE
    title = tk.Label(
        root,
        text="📊 Student Management System Pro",
        font=("Arial", 20, "bold"),
        bg="#1e1e2f",
        fg="white"
    )
    title.pack(pady=10)

    # SEARCH
    search = tk.Entry(root, width=40)
    search.pack(pady=5)

    tk.Button(root, text="🔍 Search", command=search_student, bg="black", fg="white").pack()
    tk.Button(root, text="🔄 Reset", command=reset_data).pack(pady=5)

    # INPUTS
    frame = tk.Frame(root, bg="#1e1e2f")
    frame.pack(pady=10)

    name = tk.Entry(frame, width=15)
    age = tk.Entry(frame, width=15)
    course = tk.Entry(frame, width=15)
    email = tk.Entry(frame, width=15)

    tk.Label(frame, text="Name", bg="#1e1e2f", fg="white").grid(row=0, column=0)
    name.grid(row=0, column=1)

    tk.Label(frame, text="Age", bg="#1e1e2f", fg="white").grid(row=0, column=2)
    age.grid(row=0, column=3)

    tk.Label(frame, text="Course", bg="#1e1e2f", fg="white").grid(row=0, column=4)
    course.grid(row=0, column=5)

    tk.Label(frame, text="Email", bg="#1e1e2f", fg="white").grid(row=0, column=6)
    email.grid(row=0, column=7)

    # BUTTONS
    btn_frame = tk.Frame(root, bg="#1e1e2f")
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="➕ Add", command=add_student, bg="green", fg="white").grid(row=0, column=0)
    tk.Button(btn_frame, text="✏ Update", command=update_student, bg="cyan").grid(row=0, column=1)
    tk.Button(btn_frame, text="❌ Delete", command=delete_student, bg="red", fg="white").grid(row=0, column=2)
    tk.Button(btn_frame, text="📌 Attendance", command=mark_present, bg="orange").grid(row=0, column=3)
    tk.Button(btn_frame, text="📤 Export", command=export_data, bg="blue", fg="white").grid(row=0, column=4)
    tk.Button(btn_frame, text="🛡 Backup", command=backup_db, bg="purple", fg="white").grid(row=0, column=5)

    # COUNT
    count_label = tk.Label(root, text="Total Students: 0", bg="#1e1e2f", fg="yellow", font=("Arial", 12))
    count_label.pack()

    # TABLE
    cols = ("ID", "Name", "Age", "Course", "Email")
    tree = ttk.Treeview(root, columns=cols, show="headings", height=15)

    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=180)

    tree.pack(fill=tk.BOTH, expand=True, pady=10)

    tree.bind("<ButtonRelease-1>", fill_data)

    load_students()
    root.mainloop()