import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import tkinter as tk
from tkinter import messagebox, font
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

def center_window(win, width, height):
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    win.geometry(f"{width}x{height}+{x}+{y}")

def open_course_window(username):
    window = tk.Toplevel()
    window.title("Manage Courses")
    window.resizable(True, True)
    
    width, height = 700, 450
    center_window(window, width, height)

    # Fonts
    header_font = font.Font(family="Helvetica", size=14, weight="bold")
    label_font = font.Font(family="Helvetica", size=11)
    entry_font = font.Font(family="Helvetica", size=11)

    # Header label
    tk.Label(window, text=f"Welcome: {username}", fg="blue", font=header_font).grid(row=0, column=0, columnspan=2, pady=12)

    # Form labels and entries
    tk.Label(window, text="Course Name", font=label_font).grid(row=1, column=0, sticky="e", padx=10, pady=8)
    name_entry = tk.Entry(window, width=30, font=entry_font)
    name_entry.grid(row=1, column=1, sticky="w", pady=8)

    tk.Label(window, text="Description", font=label_font).grid(row=2, column=0, sticky="e", padx=10, pady=8)
    desc_entry = tk.Entry(window, width=30, font=entry_font)
    desc_entry.grid(row=2, column=1, sticky="w", pady=8)

    tk.Button(window, text="Add Course", font=label_font,
              command=lambda: add_course(name_entry.get(), desc_entry.get())
              ).grid(row=3, column=1, sticky="w", pady=12)

    # Listbox for courses
    course_listbox = tk.Listbox(window, width=90, height=15, font=entry_font)
    course_listbox.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

    tk.Button(window, text="Refresh Course List", font=label_font,
              command=lambda: view_courses(course_listbox)).grid(row=5, column=0, columnspan=2, pady=6)

    # Delete by ID section
    tk.Label(window, text="Delete by ID", font=label_font).grid(row=6, column=0, sticky="e", padx=10, pady=8)
    delete_entry = tk.Entry(window, font=entry_font)
    delete_entry.grid(row=6, column=1, sticky="w", pady=8)

    tk.Button(window, text="Delete Course", font=label_font,
              command=lambda: delete_course(delete_entry.get())).grid(row=7, column=1, sticky="w", pady=12)

    # Allow listbox to expand when window resizes
    window.grid_rowconfigure(4, weight=1)
    window.grid_columnconfigure(1, weight=1)

    view_courses(course_listbox)
