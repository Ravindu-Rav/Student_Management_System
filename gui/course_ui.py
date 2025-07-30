# gui/course_ui.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import tkinter as tk
from tkinter import messagebox
import mysql.connector
from config import DB_CONFIG

def add_course(name, description):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO courses (course_name, description) VALUES (%s, %s)", (name, description))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Course added successfully.")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", str(err))

def delete_course(course_id):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM courses WHERE id = %s", (course_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Course deleted successfully.")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", str(err))

def view_courses(listbox):
    listbox.delete(0, tk.END)
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM courses")
        rows = cursor.fetchall()
        conn.close()
        for row in rows:
            listbox.insert(tk.END, f"ID: {row[0]} | {row[1]} | {row[2]}")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", str(err))

def open_course_window(username):

    window = tk.Toplevel()
    window.title("Manage Courses")
    window.geometry("600x400")

    tk.Label(window, text=f"Welcome: {username}", fg="blue").grid(row=0, column=0, columnspan=2, pady=5)



    # Form
    tk.Label(window, text="Course Name").grid(row=0, column=0)
    name_entry = tk.Entry(window, width=30)
    name_entry.grid(row=0, column=1)

    tk.Label(window, text="Description").grid(row=1, column=0)
    desc_entry = tk.Entry(window, width=30)
    desc_entry.grid(row=1, column=1)

    tk.Button(window, text="Add Course",
              command=lambda: add_course(name_entry.get(), desc_entry.get())
              ).grid(row=2, column=1, pady=10)

    # Listbox
    course_listbox = tk.Listbox(window, width=80)
    course_listbox.grid(row=3, column=0, columnspan=2, pady=10)

    tk.Button(window, text="Refresh Course List", command=lambda: view_courses(course_listbox)).grid(row=4, column=0, columnspan=2)

    # Delete by ID
    tk.Label(window, text="Delete by ID").grid(row=5, column=0)
    delete_entry = tk.Entry(window)
    delete_entry.grid(row=5, column=1)

    tk.Button(window, text="Delete Course", command=lambda: delete_course(delete_entry.get())).grid(row=6, column=1, pady=10)

    view_courses(course_listbox)
