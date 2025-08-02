import sys
from PySide6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QApplication, QFrame
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from student_ui import open_student_window
from course_ui import open_course_window
from grade_ui import open_grade_window
from attendance_ui import open_attendance_window
from admin_ui import open_admin_window
# Add globals for subwindows so they don’t get GC'ed
sub_windows = {}

def open_main_window(username):
    global main_window_instance
    global sub_windows

    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)

    main_window_instance = QWidget()
    window = main_window_instance
    window.setWindowTitle("Dashboard | Student Management System")
    window.setFixedSize(700, 550)

    screen = window.screen().geometry()
    center_x = int(screen.width() / 2 - window.width() / 2)
    center_y = int(screen.height() / 2 - window.height() / 2)
    window.setGeometry(center_x, center_y, 700, 550)

    main_layout = QVBoxLayout(window)
    main_layout.setContentsMargins(50, 40, 50, 40)
    main_layout.setSpacing(30)

    title_label = QLabel(f"🎓 Welcome, {username}!")
    title_label.setFont(QFont("Segoe UI", 26, QFont.Bold))
    title_label.setStyleSheet("color: #FFFFFF;")
    title_label.setAlignment(Qt.AlignCenter)

    subtitle_label = QLabel("Choose a section to manage:")
    subtitle_label.setFont(QFont("Segoe UI", 14))
    subtitle_label.setStyleSheet("color: #FFFFFF;")
    subtitle_label.setAlignment(Qt.AlignCenter)

    main_layout.addWidget(title_label)
    main_layout.addWidget(subtitle_label)

    def create_button(text, icon, handler, color="#1abc9c", hover="#16a085"):
        btn = QPushButton(f"{icon}  {text}")
        btn.setFixedHeight(50)
        btn.setFont(QFont("Segoe UI", 13, QFont.Bold))
        btn.setCursor(Qt.PointingHandCursor)
        btn.clicked.connect(handler)
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border-radius: 14px;
                border: none;
            }}
            QPushButton:hover {{
                background-color: {hover};
            }}
            QPushButton:pressed {{
                background-color: #0f6657;
            }}
        """)
        return btn

    def open_student():
        # Create and store subwindow reference to keep alive
        sub_windows['student'] = open_student_window(username,window)
        window.hide()  # hide main while sub window is open

    def open_course():
        sub_windows['course'] = open_course_window(username, window)
        window.hide()

    def open_grade():
        sub_windows['grade'] = open_grade_window(username, window)
        window.hide()

    def open_attendance():
        sub_windows['attendance'] = open_attendance_window(username, window)
        window.hide()

    def open_admin():
        sub_windows['admin'] = open_admin_window(username, window)
        window.hide()

    button_frame = QFrame()
    button_layout = QVBoxLayout(button_frame)
    button_layout.setSpacing(15)

    button_layout.addWidget(create_button("Manage Students  ", "🧑‍🎓", open_student))
    button_layout.addWidget(create_button("Manage Courses   ", "📘", open_course))
    button_layout.addWidget(create_button("Manage Grades    ", "📊", open_grade))
    button_layout.addWidget(create_button("Manage Attendance", "🗓️", open_attendance))
    button_layout.addWidget(create_button("Manage Admins    ", "👩‍💼", open_admin))
    button_layout.addWidget(create_button("Exit             ", "❌", window.close, "#e74c3c", "#c0392b"))

    main_layout.addWidget(button_frame)

    window.show()
