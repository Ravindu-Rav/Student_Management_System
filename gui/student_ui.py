# gui/student_ui.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


import tkinter as tk
from tkinter import messagebox
import mysql.connector
from config import DB_CONFIG

def add_student(name, email, phone, date):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO students (full_name, email, phone, enrollment_date) VALUES (%s, %s, %s, %s)",
                       (name, email, phone, date))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Student added successfully.")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", str(err))

def delete_student(student_id):
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

def open_student_window(username):


    tk.Label(window, text=f"Welcome: {username}", fg="blue").grid(row=0, column=0, columnspan=2, pady=5)



    window = tk.Toplevel()
    window.title("Manage Students")
    window.geometry("600x400")

    # Form
    tk.Label(window, text="Full Name").grid(row=0, column=0)
    name_entry = tk.Entry(window, width=30)
    name_entry.grid(row=0, column=1)

    tk.Label(window, text="Email").grid(row=1, column=0)
    email_entry = tk.Entry(window, width=30)
    email_entry.grid(row=1, column=1)

    tk.Label(window, text="Phone").grid(row=2, column=0)
    phone_entry = tk.Entry(window, width=30)
    phone_entry.grid(row=2, column=1)

    tk.Label(window, text="Enrollment Date (YYYY-MM-DD)").grid(row=3, column=0)
    date_entry = tk.Entry(window, width=30)
    date_entry.grid(row=3, column=1)

    tk.Button(window, text="Add Student",
              command=lambda: add_student(name_entry.get(), email_entry.get(), phone_entry.get(), date_entry.get())
              ).grid(row=4, column=1, pady=10)

    # Listbox to show students
    student_listbox = tk.Listbox(window, width=80)
    student_listbox.grid(row=5, column=0, columnspan=2, pady=10)

    tk.Button(window, text="Refresh Student List", command=lambda: view_students(student_listbox)).grid(row=6, column=0, columnspan=2)

    # Delete student section
    tk.Label(window, text="Delete by ID").grid(row=7, column=0)
    delete_entry = tk.Entry(window)
    delete_entry.grid(row=7, column=1)

    tk.Button(window, text="Delete Student", command=lambda: delete_student(delete_entry.get())).grid(row=8, column=1, pady=10)

    view_students(student_listbox)
