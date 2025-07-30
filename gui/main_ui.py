# gui/main_ui.py

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
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
    window = ttk.Window(themename="flatly")
    window.title("Student Management System - Main Menu")

    # Set fixed size window and disable resizing (no minimize/maximize)
    window_width = 500
    window_height = 500
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)
    window.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

    # Disable resizing = disables maximize and minimize buttons in most OS
    window.resizable(False, False)

    container = ttk.Frame(window, padding=30)
    container.pack(fill="both", expand=True)

    ttk.Label(container, text=f"Welcome, {username}!", font=("Helvetica", 14, "bold"), foreground="blue").pack(pady=(0, 10))
    ttk.Label(container, text="Student Management System", font=("Helvetica", 16, "bold")).pack(pady=(0, 30))

    def create_button(text, command, style=PRIMARY):
        ttk.Button(container, text=text, width=30, bootstyle=style, command=command).pack(pady=8)

    create_button("Manage Students", lambda: open_student_ui(username), SUCCESS)
    create_button("Manage Courses", lambda: open_course_ui(username), INFO)
    create_button("Manage Grades", lambda: open_grade_ui(username), WARNING)
    create_button("Manage Attendance", lambda: open_attendance_ui(username), SECONDARY)
    create_button("Manage Admins", lambda: open_admin_ui(username), DANGER)
    create_button("Exit", window.destroy, DARK)

    window.mainloop()
