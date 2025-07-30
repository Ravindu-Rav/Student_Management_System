import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import tkinter as tk
from tkinter import messagebox, font
import mysql.connector
from config import DB_CONFIG

def assign_grade(student_id, course_id, grade):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO grades (student_id, course_id, grade) VALUES (%s, %s, %s)",
                       (student_id, course_id, grade))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Grade assigned successfully.")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", str(err))

def delete_grade(grade_id):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM grades WHERE id = %s", (grade_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Grade deleted successfully.")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", str(err))

def view_grades(listbox):
    listbox.delete(0, tk.END)
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        query = """
        SELECT g.id, s.full_name, c.course_name, g.grade
        FROM grades g
        JOIN students s ON g.student_id = s.id
        JOIN courses c ON g.course_id = c.id
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()
        for row in rows:
            listbox.insert(tk.END, f"ID: {row[0]} | {row[1]} | {row[2]} | Grade: {row[3]}")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", str(err))

def center_window(win, width, height):
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    win.geometry(f"{width}x{height}+{x}+{y}")

def open_grade_window(username):
    window = tk.Toplevel()
    window.title("Manage Grades")
    window.resizable(True, True)

    width, height = 700, 450
    center_window(window, width, height)

    # Fonts
    header_font = font.Font(family="Helvetica", size=14, weight="bold")
    label_font = font.Font(family="Helvetica", size=11)
    entry_font = font.Font(family="Helvetica", size=11)

    # Header
    tk.Label(window, text=f"Welcome: {username}", fg="blue", font=header_font).grid(row=0, column=0, columnspan=2, pady=12)

    # Form labels and entries
    tk.Label(window, text="Student ID", font=label_font).grid(row=1, column=0, sticky="e", padx=10, pady=8)
    student_entry = tk.Entry(window, width=30, font=entry_font)
    student_entry.grid(row=1, column=1, sticky="w", pady=8)

    tk.Label(window, text="Course ID", font=label_font).grid(row=2, column=0, sticky="e", padx=10, pady=8)
    course_entry = tk.Entry(window, width=30, font=entry_font)
    course_entry.grid(row=2, column=1, sticky="w", pady=8)

    tk.Label(window, text="Grade (A-F)", font=label_font).grid(row=3, column=0, sticky="e", padx=10, pady=8)
    grade_entry = tk.Entry(window, width=30, font=entry_font)
    grade_entry.grid(row=3, column=1, sticky="w", pady=8)

    tk.Button(window, text="Assign Grade", font=label_font,
              command=lambda: assign_grade(student_entry.get(), course_entry.get(), grade_entry.get())
              ).grid(row=4, column=1, sticky="w", pady=12)

    # Listbox for grades
    grade_listbox = tk.Listbox(window, width=90, height=15, font=entry_font)
    grade_listbox.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

    tk.Button(window, text="Refresh Grades", font=label_font,
              command=lambda: view_grades(grade_listbox)).grid(row=6, column=0, columnspan=2, pady=6)

    # Delete grade by ID
    tk.Label(window, text="Delete by Grade ID", font=label_font).grid(row=7, column=0, sticky="e", padx=10, pady=8)
    delete_entry = tk.Entry(window, font=entry_font)
    delete_entry.grid(row=7, column=1, sticky="w", pady=8)

    tk.Button(window, text="Delete Grade", font=label_font,
              command=lambda: delete_grade(delete_entry.get())).grid(row=8, column=1, sticky="w", pady=12)

    # Enable resizing
    window.grid_rowconfigure(5, weight=1)
    window.grid_columnconfigure(1, weight=1)

    view_grades(grade_listbox)
