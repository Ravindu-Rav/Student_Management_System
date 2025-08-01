import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# gui/attendance_ui.py

import tkinter as tk
from tkinter import messagebox, font
import mysql.connector
from config import DB_CONFIG

def mark_attendance(student_id, course_id, date, status):
    if not student_id or not course_id or not date or not status:
        messagebox.showwarning("Input Error", "All fields are required.")
        return
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
    if not attendance_id:
        messagebox.showwarning("Input Error", "Attendance ID is required.")
        return
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

def center_window(win, width, height):
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    win.geometry(f"{width}x{height}+{x}+{y}")

def open_attendance_window(username, main_window):
    window = tk.Toplevel()
    window.title("Manage Attendance")
    window.geometry("1000x700")
    window.resizable(True, True)
    center_window(window, 1000, 700)

    header_font = font.Font(family="Helvetica", size=14, weight="bold")
    label_font = font.Font(family="Helvetica", size=11)
    entry_font = font.Font(family="Helvetica", size=11)

    tk.Label(window, text=f"Welcome: {username}", fg="blue", font=header_font).grid(row=0, column=0, columnspan=2, pady=10)

    tk.Label(window, text="Student ID", font=label_font).grid(row=1, column=0, sticky="e", padx=10, pady=5)
    student_entry = tk.Entry(window, width=30, font=entry_font)
    student_entry.grid(row=1, column=1, sticky="w", pady=5)

    tk.Label(window, text="Course ID", font=label_font).grid(row=2, column=0, sticky="e", padx=10, pady=5)
    course_entry = tk.Entry(window, width=30, font=entry_font)
    course_entry.grid(row=2, column=1, sticky="w", pady=5)

    tk.Label(window, text="Date (YYYY-MM-DD)", font=label_font).grid(row=3, column=0, sticky="e", padx=10, pady=5)
    date_entry = tk.Entry(window, width=30, font=entry_font)
    date_entry.grid(row=3, column=1, sticky="w", pady=5)

    tk.Label(window, text="Status (Present/Absent)", font=label_font).grid(row=4, column=0, sticky="e", padx=10, pady=5)
    status_entry = tk.Entry(window, width=30, font=entry_font)
    status_entry.grid(row=4, column=1, sticky="w", pady=5)

    tk.Button(window, text="Mark Attendance", font=label_font,
              command=lambda: mark_attendance(
                  student_entry.get(), course_entry.get(), date_entry.get(), status_entry.get()
              )).grid(row=5, column=1, pady=15, sticky="w")

    attendance_listbox = tk.Listbox(window, width=120, height=12, font=entry_font)
    attendance_listbox.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

    tk.Button(window, text="Refresh Attendance", font=label_font,
              command=lambda: view_attendance(attendance_listbox)).grid(row=7, column=0, columnspan=2, pady=5)

    tk.Label(window, text="Delete by Attendance ID", font=label_font).grid(row=8, column=0, sticky="e", padx=10, pady=5)
    delete_entry = tk.Entry(window, font=entry_font)
    delete_entry.grid(row=8, column=1, sticky="w", pady=5)

    tk.Button(window, text="Delete Attendance", font=label_font,
              command=lambda: delete_attendance(delete_entry.get())).grid(row=9, column=1, pady=15, sticky="w")

    def back_to_main():
        window.destroy()
        main_window.deiconify()

    tk.Button(window, text="Back to Main", font=label_font,
              command=back_to_main).grid(row=10, column=1, pady=10, sticky="w")

    window.grid_rowconfigure(6, weight=1)
    window.grid_columnconfigure(1, weight=1)

    view_attendance(attendance_listbox)
