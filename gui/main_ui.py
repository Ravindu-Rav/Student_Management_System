# gui/main_ui.py

import tkinter as tk
from tkinter import messagebox
from gui.student_ui import open_student_window #for the student window
from gui.course_ui import open_course_window #for the course
from gui.grade_ui import open_grade_window #for the grade
from gui.attendance_ui import open_attendance_window #for the attendance


def open_student_ui():
    open_student_window()

def open_course_ui():
    open_course_window()


def open_grade_ui():
    open_grade_window()

def open_attendance_ui():
    open_attendance_window()

def open_main_window():
    window = tk.Tk()
    window.title("Student Management System - Main Menu")
    window.geometry("400x300")
    window.resizable(False, False)

    tk.Label(window, text="Welcome to the Student Management System", font=("Helvetica", 12, "bold")).pack(pady=15)

    tk.Button(window, text="Manage Students", width=25, command=open_student_ui).pack(pady=5)
    tk.Button(window, text="Manage Courses", width=25, command=open_course_ui).pack(pady=5)
    tk.Button(window, text="Manage Grades", width=25, command=open_grade_ui).pack(pady=5)
    tk.Button(window, text="Manage Attendance", width=25, command=open_attendance_ui).pack(pady=5)
    tk.Button(window, text="Exit", width=25, command=window.destroy).pack(pady=10)

    window.mainloop()
