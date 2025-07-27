# gui/login_ui.py

import tkinter as tk
from tkinter import messagebox
import mysql.connector
from config import DB_CONFIG
from gui.main_ui import open_main_window  # You will create this next

def login():
    username = username_entry.get()
    password = password_entry.get()

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM admins WHERE username = %s AND password = %s", (username, password))
        result = cursor.fetchone()
        conn.close()

        if result:
            root.destroy()
            open_main_window()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", str(err))


# Tkinter UI setup
root = tk.Tk()
root.title("Admin Login")
root.geometry("300x200")
root.resizable(False, False)

tk.Label(root, text="Username").pack(pady=5)
username_entry = tk.Entry(root)
username_entry.pack()

tk.Label(root, text="Password").pack(pady=5)
password_entry = tk.Entry(root, show="*")
password_entry.pack()

tk.Button(root, text="Login", command=login).pack(pady=20)

root.mainloop()
