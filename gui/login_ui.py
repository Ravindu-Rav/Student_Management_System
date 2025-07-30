# gui/login_ui.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
import mysql.connector
from config import DB_CONFIG
from gui.main_ui import open_main_window

logged_in_user = None

def login():
    global logged_in_user
    username = username_entry.get()
    password = password_entry.get()

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM admins WHERE username = %s AND password = %s", (username, password))
        result = cursor.fetchone()
        conn.close()

        if result:
            logged_in_user = username
            root.destroy()
            open_main_window(logged_in_user)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", str(err))

# Setup ttkbootstrap window
root = ttk.Window(themename="flatly")  # Options: flatly, darkly, journal, morph, etc.
root.title("Admin Login")
root.geometry("400x280")
root.resizable(False, False)

# Centered frame
frame = ttk.Frame(root, padding=30)
frame.place(relx=0.5, rely=0.5, anchor=CENTER)

ttk.Label(frame, text="Admin Login", font=("Helvetica", 18, "bold")).pack(pady=(0, 20))

ttk.Label(frame, text="Username").pack(anchor=W)
username_entry = ttk.Entry(frame, width=30)
username_entry.pack(pady=(0, 10))

ttk.Label(frame, text="Password").pack(anchor=W)
password_entry = ttk.Entry(frame, show="*", width=30)
password_entry.pack(pady=(0, 20))

ttk.Button(frame, text="Login", bootstyle=PRIMARY, width=25, command=login).pack()

root.mainloop()
