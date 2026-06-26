import tkinter as tk
from tkinter import messagebox
from dashboard import open_dashboard

def check_login():
    user = entry_user.get()
    pwd = entry_pass.get()

    if user == "admin" and pwd == "admin":
        root.destroy()
        open_dashboard()
    else:
        messagebox.showerror("Error", "Invalid Username or Password")

root = tk.Tk()
root.title("Login Page")
root.geometry("300x200")

tk.Label(root, text="Username").pack()
entry_user = tk.Entry(root)
entry_user.pack()

tk.Label(root, text="Password").pack()
entry_pass = tk.Entry(root, show="*")
entry_pass.pack()

tk.Button(root, text="Login", command=check_login).pack(pady=10)

root.mainloop()