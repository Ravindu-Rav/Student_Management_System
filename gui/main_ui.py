import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from gui.student_ui import open_student_window
from gui.course_ui import open_course_window
from gui.grade_ui import open_grade_window
from gui.attendance_ui import open_attendance_window
from gui.admin_ui import open_admin_window

def open_student_ui(username, main_window):
    open_student_window(username, main_window)
    main_window.withdraw()

def open_course_ui(username, main_window):
    open_course_window(username, main_window)
    main_window.withdraw()

def open_grade_ui(username, main_window):
    open_grade_window(username, main_window)
    main_window.withdraw()

def open_attendance_ui(username, main_window):
    open_attendance_window(username, main_window)
    main_window.withdraw()

def open_admin_ui(username, main_window):
    open_admin_window(username, main_window)
    main_window.withdraw()

def open_main_window(username):
    window = ttk.Window(themename="flatly")  # same light theme
    window.title("Student Management System - Main Menu")

    window_width = 500
    window_height = 500
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)
    window.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

    window.resizable(False, False)

    container = ttk.Frame(window, padding=30)
    container.pack(fill="both", expand=True)

    # Use consistent colors: dark slate gray for text, soft lavender bg handled by theme
    dark_text_color = "#2F4F4F"
    warm_coral = "#FF6F61"

    ttk.Label(container, text=f"Welcome, {username}!", font=("Helvetica", 14, "bold"), foreground=dark_text_color).pack(pady=(0, 10))
    ttk.Label(container, text="Student Management System", font=("Helvetica", 16, "bold"), foreground=dark_text_color).pack(pady=(0, 30))

    def create_button(text, command, style=PRIMARY):
        ttk.Button(container, text=text, width=30, bootstyle=style, command=command).pack(pady=8)

    # Use warm coral (warning) for important actions, soft blues for info, neutrals for others
    create_button("Manage Students", lambda: open_student_ui(username, window), WARNING)   # coral warm
    create_button("Manage Courses", lambda: open_course_ui(username, window), INFO)         # blue info
    create_button("Manage Grades", lambda: open_grade_ui(username, window), SECONDARY)      # gray secondary
    create_button("Manage Attendance", lambda: open_attendance_ui(username, window), PRIMARY)  # default primary blue
    create_button("Manage Admins", lambda: open_admin_ui(username, window), DANGER)         # red danger for admin management
    create_button("Exit", window.destroy, SECONDARY)                                        # neutral gray exit button

    window.mainloop()
