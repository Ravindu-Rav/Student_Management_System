from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
    QMessageBox, QTableWidget, QTableWidgetItem, QApplication, QFormLayout, QFrame
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
import mysql.connector
import re
import datetime
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config import DB_CONFIG

def is_valid_date(date_str):
    try:
        datetime.datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def open_student_window(username, main_window=None):
    window = QWidget()
    window.setWindowTitle("Manage Students")
    window.setFixedSize(1000, 700)

    # Center the window
    screen = QApplication.primaryScreen().geometry()
    center_x = screen.width() // 2 - window.width() // 2
    center_y = screen.height() // 2 - window.height() // 2
    window.setGeometry(center_x, center_y, 1000, 700)

    main_layout = QVBoxLayout(window)
    main_layout.setContentsMargins(40, 30, 40, 30)
    main_layout.setSpacing(20)

    # Title
    title = QLabel(f"📋 Manage Students | Welcome, {username}")
    title.setFont(QFont("Segoe UI", 18, QFont.Bold))
    title.setStyleSheet("color: #FFFFFF;")
    title.setAlignment(Qt.AlignCenter)
    main_layout.addWidget(title)

    # Form Layout
    form_layout = QFormLayout()
    form_layout.setLabelAlignment(Qt.AlignRight)

    id_entry = QLineEdit()
    name_entry = QLineEdit()
    email_entry = QLineEdit()
    phone_entry = QLineEdit()
    date_entry = QLineEdit()

    id_entry.setPlaceholderText("For Update/Delete")
    date_entry.setPlaceholderText("YYYY-MM-DD")

    input_style = """
        QLineEdit {
            padding: 8px;
            border: 2px solid #bdc3c7;
            border-radius: 10px;
        }
        QLineEdit:focus {
            border-color: #3498db;
        }
    """
    for field in [id_entry, name_entry, email_entry, phone_entry, date_entry]:
        field.setFont(QFont("Segoe UI", 11))
        field.setStyleSheet(input_style)

    form_layout.addRow("Student ID:", id_entry)
    form_layout.addRow("Full Name:", name_entry)
    form_layout.addRow("Email:", email_entry)
    form_layout.addRow("Phone:", phone_entry)
    form_layout.addRow("Enrollment Date:", date_entry)

    form_frame = QFrame()
    form_frame.setLayout(form_layout)
    main_layout.addWidget(form_frame)

    # Student Table
    student_table = QTableWidget()
    student_table.setColumnCount(5)
    student_table.setHorizontalHeaderLabels(["ID", "Full Name", "Email", "Phone", "Enrollment Date"])
    student_table.horizontalHeader().setStretchLastSection(True)
    student_table.setEditTriggers(QTableWidget.NoEditTriggers)
    student_table.setSelectionBehavior(QTableWidget.SelectRows)
    student_table.setStyleSheet("""
        QTableWidget {
            border: 1px solid #bdc3c7;
            border-radius: 10px;
            background-color: #f9f9f9;
            color: #2c3e50;
            font-size: 12px;
        }
        QHeaderView::section {
            background-color: #2980b9;
            color: #2c3e50;
            padding: 5px;
            border: none;
        }
    """)
    main_layout.addWidget(student_table)

    # Helper functions
    def clear_fields():
        id_entry.clear()
        name_entry.clear()
        email_entry.clear()
        phone_entry.clear()
        date_entry.clear()

    def is_valid_form():
        if not name_entry.text().strip() or not email_entry.text().strip() or not phone_entry.text().strip() or not date_entry.text().strip():
            QMessageBox.warning(window, "Validation", "All fields except ID are required.")
            return False
        if not re.fullmatch(r"0\d{9}", phone_entry.text()):
            QMessageBox.warning(window, "Validation", "Phone must be a valid 10-digit number starting with 0.")
            return False
        if not is_valid_date(date_entry.text()):
            QMessageBox.warning(window, "Validation", "Date must be in YYYY-MM-DD format.")
            return False
        return True

    def refresh_table():
        student_table.setRowCount(0)
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            cursor.execute("SELECT id, full_name, email, phone, enrollment_date FROM students ORDER BY id")
            for row_idx, row_data in enumerate(cursor.fetchall()):
                student_table.insertRow(row_idx)
                for col_idx, value in enumerate(row_data):
                    item = QTableWidgetItem(str(value))
                    student_table.setItem(row_idx, col_idx, item)
            cursor.close()
            conn.close()
        except mysql.connector.Error as err:
            QMessageBox.critical(window, "Database Error", str(err))

    def add_student():
        if not is_valid_form():
            return
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO students (full_name, email, phone, enrollment_date) VALUES (%s, %s, %s, %s)",
                (name_entry.text(), email_entry.text(), phone_entry.text(), date_entry.text())
            )
            conn.commit()
            cursor.close()
            conn.close()
            QMessageBox.information(window, "Success", "Student added successfully.")
            clear_fields()
            refresh_table()
        except mysql.connector.Error as err:
            QMessageBox.critical(window, "Database Error", str(err))

    def update_student():
        sid = id_entry.text().strip()
        if not sid:
            QMessageBox.warning(window, "Validation", "Student ID is required for update.")
            return
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM students WHERE id = %s", (sid,))
            student = cursor.fetchone()
            if not student:
                QMessageBox.warning(window, "Not Found", "Student ID not found.")
                cursor.close()
                conn.close()
                return
            cursor.execute("""
                UPDATE students SET full_name=%s, email=%s, phone=%s, enrollment_date=%s
                WHERE id=%s
            """, (
                name_entry.text() or student[1],
                email_entry.text() or student[2],
                phone_entry.text() or student[3],
                date_entry.text() or str(student[4]),
                sid
            ))
            conn.commit()
            cursor.close()
            conn.close()
            QMessageBox.information(window, "Success", "Student updated successfully.")
            clear_fields()
            refresh_table()
        except mysql.connector.Error as err:
            QMessageBox.critical(window, "Database Error", str(err))

    def delete_student():
        sid = id_entry.text().strip()
        if not sid:
            QMessageBox.warning(window, "Validation", "Student ID is required for deletion.")
            return
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM students WHERE id = %s", (sid,))
            conn.commit()
            cursor.close()
            conn.close()
            QMessageBox.information(window, "Success", "Student deleted successfully.")
            clear_fields()
            refresh_table()
        except mysql.connector.Error as err:
            QMessageBox.critical(window, "Database Error", str(err))

    # Buttons
    button_layout = QHBoxLayout()
    button_layout.setSpacing(15)

    def styled_btn(label, handler, color="#3498db"):
        btn = QPushButton(label)
        btn.clicked.connect(handler)
        btn.setFixedHeight(40)
        btn.setFont(QFont("Segoe UI", 11, QFont.Bold))
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border-radius: 10px;
            }}
            QPushButton:hover {{
                background-color: #2c80b4;
            }}
        """)
        return btn

    button_layout.addWidget(styled_btn("Add Student", add_student, "#27ae60"))
    button_layout.addWidget(styled_btn("Update Student", update_student, "#f39c12"))
    button_layout.addWidget(styled_btn("Delete Student", delete_student, "#c0392b"))
    button_layout.addWidget(styled_btn("Clear Student", clear_fields, "#7f8c8d"))
    button_layout.addWidget(styled_btn("Refresh Student", refresh_table, "#2980b9"))

    main_layout.addLayout(button_layout)

    if main_window:
        def go_back():
            window.close()
            main_window.show()
        back_btn = styled_btn("⬅ Back to Dashboard", go_back, "#34495e")
        main_layout.addWidget(back_btn)

    refresh_table()
    window.show()
