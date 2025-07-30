import sys
import os
import tkinter as tk
from tkinter import messagebox, font
import mysql.connector
import datetime
import re

# Adjust path for DB config
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config import DB_CONFIG

# === Utility Functions ===
def is_valid_date(date_str):
    try:
        datetime.datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def clear_entries(entries):
    for entry in entries:
        entry.delete(0, tk.END)

# === Core Operations ===
def add_student(name, email, phone, date):
    if not name.strip() or not email.strip() or not phone.strip() or not date.strip():
        messagebox.showwarning("Validation Error", "All fields are required.")
        return
    if not re.fullmatch(r"0\d{9}", phone):
        messagebox.showwarning("Validation Error", "Phone must be a valid Sri Lankan number (10 digits starting with 0).")
        return
    if not is_valid_date(date):
        messagebox.showwarning("Validation Error", "Date must be in YYYY-MM-DD format.")
        return

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO students (full_name, email, phone, enrollment_date) VALUES (%s, %s, %s, %s)",
                       (name, email, phone, date))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Student added successfully.")
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", str(err))

def update_student(student_id, name, email, phone, date):
    if not student_id or not student_id.strip():
        messagebox.showwarning("Validation Error", "Student ID is required.")
        return

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        cursor.execute("SELECT full_name, email, phone, enrollment_date FROM students WHERE id = %s", (student_id,))
        result = cursor.fetchone()
        if not result:
            messagebox.showerror("Error", "Student ID not found.")
            conn.close()
            return

        current_name, current_email, current_phone, current_date = result

        name = name.strip() if name.strip() else current_name
        email = email.strip() if email.strip() else current_email
        phone = phone.strip() if phone.strip() else current_phone
        date = date.strip() if date.strip() else str(current_date)

        if not re.fullmatch(r"0\d{9}", phone):
            messagebox.showwarning("Validation Error", "Phone must be a valid Sri Lankan number (10 digits starting with 0).")
            conn.close()
            return
        if not is_valid_date(date):
            messagebox.showwarning("Validation Error", "Date must be in YYYY-MM-DD format.")
            conn.close()
            return

        cursor.execute("""
            UPDATE students
            SET full_name = %s, email = %s, phone = %s, enrollment_date = %s
            WHERE id = %s
        """, (name, email, phone, date, student_id))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Student updated successfully.")
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", str(err))

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
            listbox.insert(tk.END, f"{row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]}")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", str(err))

def center_window(win, width, height):
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    win.geometry(f"{width}x{height}+{x}+{y}")

def open_student_window(username, main_window):
    window = tk.Toplevel()
    window.title("Manage Students")
    width, height = 1000, 700
    center_window(window, width, height)

    header_font = font.Font(family="Helvetica", size=14, weight="bold")
    label_font = font.Font(family="Helvetica", size=11)
    entry_font = font.Font(family="Helvetica", size=11)

    tk.Label(window, text=f"Welcome: {username}", fg="blue", font=header_font).grid(row=0, column=0, columnspan=2, pady=10)

    labels = ["ID (for Update)", "Full Name", "Email", "Phone", "Enrollment Date (YYYY-MM-DD)"]
    entries = []
    for i, label_text in enumerate(labels):
        tk.Label(window, text=label_text, font=label_font).grid(row=i+1, column=0, sticky="e", padx=10, pady=5)
        entry = tk.Entry(window, width=35, font=entry_font)
        entry.grid(row=i+1, column=1, sticky="w", pady=5)
        entries.append(entry)

    student_id_entry, name_entry, email_entry, phone_entry, date_entry = entries

    tk.Button(window, text="Add Student", font=label_font,
              command=lambda: add_student(name_entry.get(), email_entry.get(), phone_entry.get(), date_entry.get())
              ).grid(row=6, column=1, sticky="w", pady=10)

    tk.Button(window, text="Update Student", font=label_font,
              command=lambda: update_student(student_id_entry.get(), name_entry.get(), email_entry.get(), phone_entry.get(), date_entry.get())
              ).grid(row=7, column=1, sticky="w", pady=5)

    tk.Button(window, text="Clear Fields", font=label_font,
              command=lambda: clear_entries(entries)).grid(row=8, column=1, sticky="w", pady=5)

    student_listbox = tk.Listbox(window, width=120, height=15, font=entry_font)
    student_listbox.grid(row=9, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

    tk.Button(window, text="Refresh List", font=label_font,
              command=lambda: view_students(student_listbox)).grid(row=10, column=0, columnspan=2, pady=5)

    tk.Label(window, text="Delete by ID", font=label_font).grid(row=11, column=0, sticky="e", padx=10, pady=5)
    delete_entry = tk.Entry(window, font=entry_font)
    delete_entry.grid(row=11, column=1, sticky="w", pady=5)

    tk.Button(window, text="Delete Student", font=label_font,
              command=lambda: delete_student(delete_entry.get())).grid(row=12, column=1, sticky="w", pady=5)

    def back_to_main():
        window.destroy()
        main_window.deiconify()

    back_btn = tk.Button(window, text="Back to Main", font=label_font, command=back_to_main)
    back_btn.grid(row=13, column=1, sticky="w", pady=15)

    window.protocol("WM_DELETE_WINDOW", back_to_main)

    window.grid_rowconfigure(9, weight=1)
    window.grid_columnconfigure(1, weight=1)

    view_students(student_listbox)
