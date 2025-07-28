import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# gui/admin_ui.py

import tkinter as tk
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
    listbox.delete(0, tk.END)
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SELECT id, username FROM admins")
        rows = cursor.fetchall()
        conn.close()
        for row in rows:
            listbox.insert(tk.END, f"ID: {row[0]} | Username: {row[1]}")
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
    
    window = tk.Toplevel()
    window.title("Manage Students")
    window.geometry("600x400")

    tk.Label(window, text=f"Logged in as: {username}", fg="blue").grid(row=0, column=0, columnspan=2, pady=5)



    window = tk.Toplevel()
    window.title("Admin Management")
    window.geometry("500x400")

    # Form to add new admin
    tk.Label(window, text="Username").grid(row=0, column=0)
    username_entry = tk.Entry(window, width=30)
    username_entry.grid(row=0, column=1)

    tk.Label(window, text="Password").grid(row=1, column=0)
    password_entry = tk.Entry(window, width=30, show="*")
    password_entry.grid(row=1, column=1)

    tk.Button(window, text="Add Admin",
              command=lambda: add_admin(username_entry.get(), password_entry.get())
              ).grid(row=2, column=1, pady=10)

    # Admin List
    admin_listbox = tk.Listbox(window, width=60)
    admin_listbox.grid(row=3, column=0, columnspan=2, pady=10)

    tk.Button(window, text="Refresh Admin List", command=lambda: view_admins(admin_listbox)).grid(row=4, column=0, columnspan=2)

    # Delete admin
    tk.Label(window, text="Delete Admin ID").grid(row=5, column=0)
    delete_entry = tk.Entry(window)
    delete_entry.grid(row=5, column=1)

    tk.Button(window, text="Delete Admin", command=lambda: delete_admin(delete_entry.get())).grid(row=6, column=1, pady=10)

    view_admins(admin_listbox)
