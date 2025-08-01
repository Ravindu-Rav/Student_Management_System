import sys
import os
import tkinter as tk
from tkinter import messagebox, font
import mysql.connector
import re
from config import DB_CONFIG

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# === DB Operations ===
def add_admin(username, password):
    if not username.strip() or not password.strip():
        messagebox.showwarning("Validation Error", "Username and password are required.")
        return
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
    if not admin_id.strip().isdigit():
        messagebox.showwarning("Validation Error", "Please enter a valid numeric Admin ID.")
        return
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM admins WHERE id = %s", (admin_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Admin deleted successfully.")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", str(err))

def center_window(win, width, height):
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    win.geometry(f"{width}x{height}+{x}+{y}")

# === Main Admin Window ===
def open_admin_window(username, main_window):
    window = tk.Toplevel()
    window.title("Admin Management")
    width, height = 900, 600
    center_window(window, width, height)

    header_font = font.Font(family="Helvetica", size=14, weight="bold")
    label_font = font.Font(family="Helvetica", size=11)
    entry_font = font.Font(family="Helvetica", size=11)

    tk.Label(window, text=f"Welcome: {username}", fg="blue", font=header_font).grid(row=0, column=0, columnspan=2, pady=10)

    # === Entry Fields ===
    tk.Label(window, text="Username", font=label_font).grid(row=1, column=0, sticky="e", padx=10, pady=5)
    username_entry = tk.Entry(window, width=35, font=entry_font)
    username_entry.grid(row=1, column=1, sticky="w", pady=5)

    tk.Label(window, text="Password", font=label_font).grid(row=2, column=0, sticky="e", padx=10, pady=5)
    password_entry = tk.Entry(window, width=35, font=entry_font, show="*")
    password_entry.grid(row=2, column=1, sticky="w", pady=5)

    tk.Button(window, text="Add Admin", font=label_font,
              command=lambda: add_admin(username_entry.get(), password_entry.get())
              ).grid(row=3, column=1, sticky="w", pady=10)

    # === Admin Listbox ===
    tk.Label(window, text="Admin List", font=label_font).grid(row=4, column=0, columnspan=2, pady=10)
    admin_listbox = tk.Listbox(window, width=70, height=10, font=entry_font)
    admin_listbox.grid(row=5, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")

    tk.Button(window, text="Refresh Admin List", font=label_font,
              command=lambda: view_admins(admin_listbox)).grid(row=6, column=0, columnspan=2, pady=5)

    # === Delete Admin ===
    tk.Label(window, text="Delete Admin ID", font=label_font).grid(row=7, column=0, sticky="e", padx=10, pady=5)
    delete_entry = tk.Entry(window, width=20, font=entry_font)
    delete_entry.grid(row=7, column=1, sticky="w", pady=5)

    tk.Button(window, text="Delete Admin", font=label_font,
              command=lambda: delete_admin(delete_entry.get())).grid(row=8, column=1, sticky="w", pady=5)

    # === Back Button ===
    def back_to_main():
        window.destroy()
        main_window.deiconify()

    back_btn = tk.Button(window, text="Back to Main", font=label_font, command=back_to_main)
    back_btn.grid(row=9, column=1, sticky="w", pady=15)

    window.protocol("WM_DELETE_WINDOW", back_to_main)
    window.grid_rowconfigure(5, weight=1)
    window.grid_columnconfigure(1, weight=1)

    view_admins(admin_listbox)
