# gui/login_ui.py
import sys

from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QMessageBox, QFrame
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
import mysql.connector
from config import DB_CONFIG
from main_ui import open_main_window

logged_in_user = None

def login():
    global logged_in_user
    username = username_entry.text().strip()
    password = password_entry.text().strip()

    if not username or not password:
        QMessageBox.warning(window, "Input Error", "Please enter both username and password.")
        return

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM admins WHERE username = %s AND password = %s", (username, password))
        result = cursor.fetchone()
        conn.close()

        if result:
            admin_id = result[0]  # ID from admins table
            logged_in_user = username
            QMessageBox.information(window, "Login Successful", f"Welcome {username}!")
            window.close()
            open_main_window(logged_in_user, admin_id)
        else:
            QMessageBox.critical(window, "Login Failed", "Invalid username or password.")
    except mysql.connector.Error as err:
        QMessageBox.critical(window, "Database Error", str(err))


app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("Admin Login")
window.setFixedSize(600, 500)

# Center window
screen = app.primaryScreen().geometry()
center_x = int(screen.width() / 2 - window.width() / 2)
center_y = int(screen.height() / 2 - window.height() / 2)
window.setGeometry(center_x, center_y, 600, 400)

# Main vertical layout
main_layout = QVBoxLayout(window)
main_layout.setContentsMargins(80, 60, 80, 60)
main_layout.setSpacing(30)

# Title
title_label = QLabel("👋 Welcome Back!")
title_label.setFont(QFont("Segoe UI", 28, QFont.Bold))
title_label.setAlignment(Qt.AlignCenter)
title_label.setStyleSheet("color: #FFFFFF;")
main_layout.addWidget(title_label)

# Subtitle
subtitle_label = QLabel("Log in to your admin account")
subtitle_label.setFont(QFont("Segoe UI", 14))
subtitle_label.setAlignment(Qt.AlignCenter)
subtitle_label.setStyleSheet("color: #FFFFFF;")
main_layout.addWidget(subtitle_label)

# Username input frame with emoji icon
username_frame = QFrame()
username_layout = QHBoxLayout(username_frame)
username_layout.setContentsMargins(0, 0, 0, 0)
username_layout.setSpacing(10)

username_icon = QLabel("👤")
username_icon.setFont(QFont("Segoe UI Emoji", 18))
username_icon.setFixedWidth(30)
username_icon.setAlignment(Qt.AlignCenter)
username_layout.addWidget(username_icon)

username_entry = QLineEdit()
username_entry.setPlaceholderText("Username")
username_entry.setFont(QFont("Segoe UI", 12))
username_entry.setStyleSheet("""
    QLineEdit {
        border: 2px solid #1abc9c;
        border-radius: 12px;
        padding: 10px 12px;
        background-color: #eafaf7;
        color: #16a085;
        selection-background-color: #1abc9c;
    }
    QLineEdit:focus {
        border-color: #16a085;
        background-color: #d0f1eb;
    }
""")
username_layout.addWidget(username_entry)

main_layout.addWidget(username_frame)

# Password input frame with emoji icon
password_frame = QFrame()
password_layout = QHBoxLayout(password_frame)
password_layout.setContentsMargins(0, 0, 0, 0)
password_layout.setSpacing(10)

password_icon = QLabel("🔒")
password_icon.setFont(QFont("Segoe UI Emoji", 18))
password_icon.setFixedWidth(30)
password_icon.setAlignment(Qt.AlignCenter)
password_layout.addWidget(password_icon)

password_entry = QLineEdit()
password_entry.setEchoMode(QLineEdit.Password)
password_entry.setPlaceholderText("Password")
password_entry.setFont(QFont("Segoe UI", 12))
password_entry.setStyleSheet("""
    QLineEdit {
        border: 2px solid #1abc9c;
        border-radius: 12px;
        padding: 10px 12px;
        background-color: #eafaf7;
        color: #16a085;
        selection-background-color: #1abc9c;
    }
    QLineEdit:focus {
        border-color: #16a085;
        background-color: #d0f1eb;
    }
""")
password_layout.addWidget(password_entry)

main_layout.addWidget(password_frame)

# Login button
login_button = QPushButton("Login")
login_button.setFixedHeight(50)
login_button.setFont(QFont("Segoe UI", 14, QFont.Bold))
login_button.setCursor(Qt.PointingHandCursor)
login_button.clicked.connect(login)
login_button.setStyleSheet("""
    QPushButton {
        background-color: #e67e22;
        color: white;
        border-radius: 14px;
        border: none;
        transition: background-color 0.3s ease;
    }
    QPushButton:hover {
        background-color: #d35400;
    }
    QPushButton:pressed {
        background-color: #a84300;
    }
""")
main_layout.addWidget(login_button)

window.show()
sys.exit(app.exec())
