# gui/main_ui.py

import tkinter as tk
from tkinter import messagebox
from gui.student_ui import open_student_window
from gui.course_ui import open_course_window
from gui.grade_ui import open_grade_window
from gui.attendance_ui import open_attendance_window
from gui.admin_ui import open_admin_window

def open_student_ui(username):
    open_student_window(username)

def open_course_ui(username):
    open_course_window(username)

def open_grade_ui(username):
    open_grade_window(username)

def open_attendance_ui(username):
    open_attendance_window(username)

def open_admin_ui(username):
    open_admin_window(username)

def open_main_window(username):
    window = tk.Tk()
    window.title("Student Management System - Main Menu")
    window.geometry("400x400")
    window.resizable(False, False)

    # Show the logged-in user
    tk.Label(window, text=f"Welcome: {username}", fg="blue").pack(pady=5)
    tk.Label(window, text="Welcome to the Student Management System", font=("Helvetica", 12, "bold")).pack(pady=10)

    # Buttons
    tk.Button(window, text="Manage Students", width=25, command=lambda: open_student_ui(username)).pack(pady=5)
    tk.Button(window, text="Manage Courses", width=25, command=lambda: open_course_ui(username)).pack(pady=5)
    tk.Button(window, text="Manage Grades", width=25, command=lambda: open_grade_ui(username)).pack(pady=5)
    tk.Button(window, text="Manage Attendance", width=25, command=lambda: open_attendance_ui(username)).pack(pady=5)
    tk.Button(window, text="Manage Admins", width=25, command=lambda: open_admin_ui(username)).pack(pady=5)
    tk.Button(window, text="Exit", width=25, command=window.destroy).pack(pady=10)

    window.mainloop()
