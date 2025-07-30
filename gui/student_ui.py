import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import tkinter as tk
from tkinter import messagebox, font
from ttkbootstrap import DateEntry
import mysql.connector
from config import DB_CONFIG
import datetime

def is_valid_date(date_str):
    try:
        datetime.datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def is_valid_sri_lankan_phone(phone):
    return phone.isdigit() and len(phone) == 10 and phone.startswith("0")

def add_student(name, email, phone, date):
    if not name.strip():
        messagebox.showwarning("Validation Error", "Full Name cannot be empty.")
        return
    if not email.strip():
        messagebox.showwarning("Validation Error", "Email cannot be empty.")
        return
    if not phone.strip():
        messagebox.showwarning("Validation Error", "Phone cannot be empty.")
        return
    if not date.strip():
        messagebox.showwarning("Validation Error", "Enrollment Date cannot be empty.")
        return

    if not is_valid_sri_lankan_phone(phone):
        messagebox.showwarning("Validation Error", "Phone number must be a valid Sri Lankan number (10 digits starting with 0).")
        return

    if not is_valid_date(date):
        messagebox.showwarning("Validation Error", "Enrollment Date must be in YYYY-MM-DD format.")
        return

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO students (full_name, email, phone, enrollment_date) VALUES (%s, %s, %s, %s)",
            (name, email, phone, date)
        )
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Student added successfully.")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", str(err))

def delete_student(student_id):
    if not student_id.strip():
        messagebox.showwarning("Validation Error", "Please enter a student ID to delete.")
        return

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM students WHERE id = %s", (student_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Student deleted successfully.")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", str(err))

def view_students(listbox):
    listbox.delete(0, tk.END)
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students")
        rows = cursor.fetchall()
        conn.close()
        for row in rows:
            listbox.insert(tk.END, f"ID: {row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]}")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", str(err))

def center_window(win, width, height):
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    win.geometry(f"{width}x{height}+{x}+{y}")

def open_student_window(username):
    window = tk.Toplevel()
    window.title("Manage Students")
    window.resizable(True, True)

    width, height = 700, 450
    center_window(window, width, height)

    # Fonts
    header_font = font.Font(family="Helvetica", size=14, weight="bold")
    label_font = font.Font(family="Helvetica", size=11)
    entry_font = font.Font(family="Helvetica", size=11)

    # Header
    tk.Label(window, text=f"Welcome: {username}", fg="blue", font=header_font).grid(row=0, column=0, columnspan=2, pady=12)

    # Form Labels & Entries
    tk.Label(window, text="Full Name", font=label_font).grid(row=1, column=0, sticky="e", padx=10, pady=8)
    name_entry = tk.Entry(window, width=30, font=entry_font)
    name_entry.grid(row=1, column=1, sticky="w", pady=8)

    tk.Label(window, text="Email", font=label_font).grid(row=2, column=0, sticky="e", padx=10, pady=8)
    email_entry = tk.Entry(window, width=30, font=entry_font)
    email_entry.grid(row=2, column=1, sticky="w", pady=8)

    tk.Label(window, text="Phone", font=label_font).grid(row=3, column=0, sticky="e", padx=10, pady=8)
    phone_entry = tk.Entry(window, width=30, font=entry_font)
    phone_entry.grid(row=3, column=1, sticky="w", pady=8)

    tk.Label(window, text="Enrollment Date", font=label_font).grid(row=4, column=0, sticky="e", padx=10, pady=8)
    date_entry = DateEntry(window, width=27, bootstyle="info", dateformat="%Y-%m-%d")
    date_entry.grid(row=4, column=1, sticky="w", pady=8)

    tk.Button(window, text="Add Student", font=label_font,
              command=lambda: add_student(name_entry.get(), email_entry.get(), phone_entry.get(), date_entry.entry.get())
              ).grid(row=5, column=1, sticky="w", pady=12)

    # Listbox for Students
    student_listbox = tk.Listbox(window, width=90, height=15, font=entry_font)
    student_listbox.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

    tk.Button(window, text="Refresh Student List", font=label_font,
              command=lambda: view_students(student_listbox)).grid(row=7, column=0, columnspan=2, pady=6)

    # Delete by ID
    tk.Label(window, text="Delete by ID", font=label_font).grid(row=8, column=0, sticky="e", padx=10, pady=8)
    delete_entry = tk.Entry(window, font=entry_font)
    delete_entry.grid(row=8, column=1, sticky="w", pady=8)

    tk.Button(window, text="Delete Student", font=label_font,
              command=lambda: delete_student(delete_entry.get())).grid(row=9, column=1, sticky="w", pady=12)

    # Make listbox expand on resize
    window.grid_rowconfigure(6, weight=1)
    window.grid_columnconfigure(1, weight=1)

    view_students(student_listbox)
