# gui/grade_ui.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


import tkinter as tk
from tkinter import messagebox
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

def open_grade_window(username):

    window = tk.Toplevel()
    window.title("Manage Grades")
    window.geometry("600x400")

    
    tk.Label(window, text=f"Welcome: {username}", fg="blue").grid(row=0, column=0, columnspan=2, pady=5)


    # Form
    tk.Label(window, text="Student ID").grid(row=0, column=0)
    student_entry = tk.Entry(window, width=30)
    student_entry.grid(row=0, column=1)

    tk.Label(window, text="Course ID").grid(row=1, column=0)
    course_entry = tk.Entry(window, width=30)
    course_entry.grid(row=1, column=1)

    tk.Label(window, text="Grade (A-F)").grid(row=2, column=0)
    grade_entry = tk.Entry(window, width=30)
    grade_entry.grid(row=2, column=1)

    tk.Button(window, text="Assign Grade",
              command=lambda: assign_grade(student_entry.get(), course_entry.get(), grade_entry.get())
              ).grid(row=3, column=1, pady=10)

    # Listbox
    grade_listbox = tk.Listbox(window, width=80)
    grade_listbox.grid(row=4, column=0, columnspan=2, pady=10)

    tk.Button(window, text="Refresh Grades", command=lambda: view_grades(grade_listbox)).grid(row=5, column=0, columnspan=2)

    # Delete
    tk.Label(window, text="Delete by Grade ID").grid(row=6, column=0)
    delete_entry = tk.Entry(window)
    delete_entry.grid(row=6, column=1)

    tk.Button(window, text="Delete Grade", command=lambda: delete_grade(delete_entry.get())).grid(row=7, column=1, pady=10)

    view_grades(grade_listbox)
