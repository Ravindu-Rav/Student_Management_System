import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox, PhotoImage
import mysql.connector
from config import DB_CONFIG
from gui.main_ui import open_main_window

logged_in_user = None

def login():
    global logged_in_user
    username = username_entry.get().strip()
    password = password_entry.get().strip()

    if not username or not password:
        messagebox.showwarning("Input Error", "Please enter both username and password.")
        return

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

# -------- UI Setup --------
root = ttk.Window(themename="flatly")  # Light modern theme
root.title("Admin Login")
root.resizable(False, False)

window_width = 800
window_height = 500
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
center_x = int(screen_width / 2 - window_width / 2)
center_y = int(screen_height / 2 - window_height / 2)
root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

# Configure grid layout for 2 columns
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=2)
root.rowconfigure(0, weight=1)

# Left Panel with soft lavender background (#E6E6FA) and icon + text
left_frame = ttk.Frame(root, padding=30)
left_frame.grid(row=0, column=0, sticky="nsew")
left_frame.configure(style="LeftPanel.TFrame")

# Load and display image or emoji icon (replace with your image path)
try:
    icon_img = PhotoImage(file="assets/admin_icon.png")  # Replace with your image path
    icon_label = ttk.Label(left_frame, image=icon_img, background="#E6E6FA")
    icon_label.image = icon_img  # prevent GC
    icon_label.pack(pady=(10, 10))
except Exception:
    icon_label = ttk.Label(left_frame, text="👩‍💻", font=("Segoe UI Emoji", 80), foreground="#2F4F4F", background="#E6E6FA")
    icon_label.pack(pady=(10, 10))

title_label = ttk.Label(left_frame, text="Student\nManagement", font=("Helvetica", 24, "bold"), foreground="#2F4F4F", background="#E6E6FA", justify="center")
title_label.pack(pady=(0, 5))

subtitle_label = ttk.Label(left_frame, text="Admin Portal", font=("Helvetica", 14), foreground="#2F4F4F", background="#E6E6FA")
subtitle_label.pack()

# Right Panel with white background and form card effect
right_frame = ttk.Frame(root, padding=40, bootstyle="light")
right_frame.grid(row=0, column=1, sticky="nsew")

form_frame = ttk.Frame(right_frame, padding=20, bootstyle="white")
form_frame.pack(expand=True, fill="both", padx=20, pady=20)

ttk.Label(form_frame, text="Admin Login", font=("Helvetica", 22, "bold"), foreground="#2F4F4F").pack(pady=(0, 30))

ttk.Label(form_frame, text="Username:", font=("Helvetica", 12), foreground="#2F4F4F").pack(anchor="w")
username_entry = ttk.Entry(form_frame, width=35, font=("Helvetica", 12))
username_entry.pack(pady=(0, 15))
username_entry.focus()

ttk.Label(form_frame, text="Password:", font=("Helvetica", 12), foreground="#2F4F4F").pack(anchor="w")
password_entry = ttk.Entry(form_frame, show="*", width=35, font=("Helvetica", 12))
password_entry.pack(pady=(0, 25))

login_btn = ttk.Button(form_frame, text="Login", bootstyle="warning", width=30, command=login)  # warning = warm coral
login_btn.pack()

def on_enter(e):
    login_btn.configure(bootstyle="warning-inverse")

def on_leave(e):
    login_btn.configure(bootstyle="warning")

login_btn.bind("<Enter>", on_enter)
login_btn.bind("<Leave>", on_leave)

# Style config for left panel bg color soft lavender
style = ttk.Style()
style.configure("LeftPanel.TFrame", background="#E6E6FA")

root.mainloop()
