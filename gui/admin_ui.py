# gui/admin_ui.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
import mysql.connector
from config import DB_CONFIG

def add_admin(username, password):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO admins (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Admin added successfully.")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", str(err))

def view_admins(listbox):
    listbox.delete(0, ttk.END)
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SELECT id, username FROM admins")
        rows = cursor.fetchall()
        conn.close()
        for row in rows:
            listbox.insert(ttk.END, f"ID: {row[0]} | Username: {row[1]}")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", str(err))

def delete_admin(admin_id):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM admins WHERE id = %s", (admin_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Admin deleted successfully.")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", str(err))

def open_admin_window(username):
    window = ttk.Toplevel(themename="flatly")  # Theme: flatly (light), use 'darkly' or 'superhero' for dark themes
    window.title("Admin Management")

    # Set size and center the window
    window_width = 700
    window_height = 550
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)
    window.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

    window.resizable(True, True)  # Enable maximize/minimize

    # Main container
    container = ttk.Frame(window, padding=20)
    container.pack(fill=BOTH, expand=True)

    ttk.Label(container, text=f"Welcome: {username}", font=("Helvetica", 14, "bold"), foreground="blue").pack(anchor=W, pady=(0, 15))

    # Admin form
    form_frame = ttk.Frame(container)
    form_frame.pack(fill=X, pady=10)

    ttk.Label(form_frame, text="Username").grid(row=0, column=0, sticky=W, padx=5, pady=8)
    username_entry = ttk.Entry(form_frame, width=40)
    username_entry.grid(row=0, column=1, padx=5, pady=8)

    ttk.Label(form_frame, text="Password").grid(row=1, column=0, sticky=W, padx=5, pady=8)
    password_entry = ttk.Entry(form_frame, width=40, show="*")
    password_entry.grid(row=1, column=1, padx=5, pady=8)

    ttk.Button(form_frame, text="Add Admin", bootstyle=SUCCESS,
               command=lambda: add_admin(username_entry.get(), password_entry.get())
               ).grid(row=2, column=1, sticky=E, padx=5, pady=10)

    # Admin list
    ttk.Label(container, text="Admin List:").pack(anchor=W, pady=(15, 5))
    admin_listbox = ttk.Text(container, height=10, font=("Courier New", 10))
    admin_listbox.pack(fill=BOTH, expand=True, padx=5, pady=5)

    # Replacing Text widget with Listbox
    admin_listbox = tk.Listbox(container, height=10, font=("Courier New", 10))
    admin_listbox.pack(fill=BOTH, expand=True, padx=5, pady=5)

    ttk.Button(container, text="Refresh Admin List", bootstyle=INFO,
               command=lambda: view_admins(admin_listbox)).pack(pady=(5, 15))

    # Delete admin
    delete_frame = ttk.Frame(container)
    delete_frame.pack(fill=X, pady=10)

    ttk.Label(delete_frame, text="Delete Admin ID").grid(row=0, column=0, sticky=W, padx=5)
    delete_entry = ttk.Entry(delete_frame, width=20)
    delete_entry.grid(row=0, column=1, padx=5)

    ttk.Button(delete_frame, text="Delete Admin", bootstyle=DANGER,
               command=lambda: delete_admin(delete_entry.get())).grid(row=0, column=2, padx=10)

    # Load initial data
    view_admins(admin_listbox)
