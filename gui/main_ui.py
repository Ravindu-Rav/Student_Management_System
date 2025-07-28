# gui/main_ui.py

import tkinter as tk
from tkinter import messagebox
from gui.student_ui import open_student_window

def open_student_ui():
    open_student_window()

def open_course_ui():
    messagebox.showinfo("Course", "Course Management UI coming soon!")

def open_grade_ui():
    messagebox.showinfo("Grades", "Grades Management UI coming soon!")

def open_attendance_ui():
    messagebox.showinfo("Attendance", "Attendance Management UI coming soon!")

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
