import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# gui/attendance_ui.py

import tkinter as tk
from tkinter import messagebox
import mysql.connector
from config import DB_CONFIG

def mark_attendance(student_id, course_id, date, status):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO attendance (student_id, course_id, date, status) VALUES (%s, %s, %s, %s)",
            (student_id, course_id, date, status)
        )
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Attendance marked successfully.")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", str(err))

def delete_attendance(attendance_id):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM attendance WHERE id = %s", (attendance_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Attendance record deleted.")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", str(err))

def view_attendance(listbox):
    listbox.delete(0, tk.END)
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        query = """
        SELECT a.id, s.full_name, c.course_name, a.date, a.status
        FROM attendance a
        JOIN students s ON a.student_id = s.id
        JOIN courses c ON a.course_id = c.id
        ORDER BY a.date DESC
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()
        for row in rows:
            listbox.insert(tk.END, f"ID: {row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]}")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", str(err))

def open_attendance_window():
    window = tk.Toplevel()
    window.title("Manage Attendance")
    window.geometry("700x400")

    # Form
    tk.Label(window, text="Student ID").grid(row=0, column=0)
    student_entry = tk.Entry(window, width=30)
    student_entry.grid(row=0, column=1)

    tk.Label(window, text="Course ID").grid(row=1, column=0)
    course_entry = tk.Entry(window, width=30)
    course_entry.grid(row=1, column=1)

    tk.Label(window, text="Date (YYYY-MM-DD)").grid(row=2, column=0)
    date_entry = tk.Entry(window, width=30)
    date_entry.grid(row=2, column=1)

    tk.Label(window, text="Status (Present/Absent)").grid(row=3, column=0)
    status_entry = tk.Entry(window, width=30)
    status_entry.grid(row=3, column=1)

    tk.Button(window, text="Mark Attendance",
              command=lambda: mark_attendance(
                  student_entry.get(), course_entry.get(), date_entry.get(), status_entry.get()
              )).grid(row=4, column=1, pady=10)

    # Listbox
    attendance_listbox = tk.Listbox(window, width=100)
    attendance_listbox.grid(row=5, column=0, columnspan=2, pady=10)

    tk.Button(window, text="Refresh Attendance", command=lambda: view_attendance(attendance_listbox)).grid(row=6, column=0, columnspan=2)

    # Delete section
    tk.Label(window, text="Delete by Attendance ID").grid(row=7, column=0)
    delete_entry = tk.Entry(window)
    delete_entry.grid(row=7, column=1)

    tk.Button(window, text="Delete Attendance", command=lambda: delete_attendance(delete_entry.get())).grid(row=8, column=1, pady=10)

    view_attendance(attendance_listbox)
