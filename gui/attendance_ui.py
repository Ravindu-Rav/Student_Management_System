import sys
import mysql.connector
from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
    QMessageBox, QTableWidget, QTableWidgetItem, QApplication, QFormLayout,
    QFrame
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

from config import DB_CONFIG

def open_attendance_window(username, main_window=None):
    window = QWidget()
    window.setWindowTitle("Attendance Management")
    window.setFixedSize(1000, 700)

    # Center window
    screen = QApplication.primaryScreen().geometry()
    center_x = int(screen.width() / 2 - window.width() / 2)
    center_y = int(screen.height() / 2 - window.height() / 2)
    window.setGeometry(center_x, center_y, window.width(), window.height())

    main_layout = QVBoxLayout(window)
    main_layout.setContentsMargins(40, 30, 40, 30)
    main_layout.setSpacing(20)

    # Title
    title = QLabel(f"📅 Attendance Management | Welcome, {username}")
    title.setFont(QFont("Segoe UI", 18, QFont.Bold))
    title.setStyleSheet("color: #FFFFFF;")
    title.setAlignment(Qt.AlignCenter)
    main_layout.addWidget(title)

    # Form
    form_layout = QFormLayout()
    student_id_entry = QLineEdit()
    date_entry = QLineEdit()
    status_entry = QLineEdit()

    for field in [student_id_entry, date_entry, status_entry]:
        field.setFont(QFont("Segoe UI", 11))
        field.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 2px solid #bdc3c7;
                border-radius: 10px;
            }
            QLineEdit:focus {
                border-color: #3498db;
            }
        """)

    date_entry.setPlaceholderText("YYYY-MM-DD")
    status_entry.setPlaceholderText("Present / Absent")

    form_layout.addRow("Student ID:", student_id_entry)
    form_layout.addRow("Date:", date_entry)
    form_layout.addRow("Status:", status_entry)
    form_frame = QFrame()
    form_frame.setLayout(form_layout)
    main_layout.addWidget(form_frame)

    # Table
    attendance_table = QTableWidget()
    attendance_table.setColumnCount(4)
    attendance_table.setHorizontalHeaderLabels(["ID", "Student ID", "Date", "Status"])
    attendance_table.setFont(QFont("Segoe UI", 10))
    attendance_table.setStyleSheet("""
        QTableWidget {
            border: 2px solid #bdc3c7;
            border-radius: 10px;
            background-color: #fdfdfd;
            color: #2c3e50;
            gridline-color: #dcdcdc;
        }
        QHeaderView::section {
            background-color: #3498db;
            color: #2c3e50;
            font-weight: bold;
            padding: 5px;
        }
    """)
    main_layout.addWidget(attendance_table)

    delete_entry = QLineEdit()
    delete_entry.setPlaceholderText("Attendance ID to delete or update")
    delete_entry.setFont(QFont("Segoe UI", 11))
    delete_entry.setStyleSheet("""
        QLineEdit {
            padding: 8px;
            border: 2px solid #bdc3c7;
            border-radius: 10px;
        }
        QLineEdit:focus {
            border-color: #c0392b;
        }
    """)
    main_layout.addWidget(delete_entry)

    def styled_btn(text, color, handler):
        btn = QPushButton(text)
        btn.setFont(QFont("Segoe UI", 11, QFont.Bold))
        btn.setFixedHeight(40)
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
        btn.clicked.connect(handler)
        return btn

    def refresh_list():
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            cursor.execute("SELECT id, student_id, date, status FROM attendance ORDER BY id ASC")
            rows = cursor.fetchall()
            cursor.close()
            conn.close()

            attendance_table.setRowCount(len(rows))
            for row_idx, row_data in enumerate(rows):
                for col_idx, value in enumerate(row_data):
                    item = QTableWidgetItem(str(value))
                    attendance_table.setItem(row_idx, col_idx, item)
        except mysql.connector.Error as err:
            QMessageBox.critical(window, "Database Error", str(err))

    def add_attendance():
        student_id = student_id_entry.text().strip()
        date = date_entry.text().strip()
        status = status_entry.text().strip()

        if not student_id or not date or not status:
            QMessageBox.warning(window, "Validation", "All fields are required.")
            return
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO attendance (student_id, date, status) VALUES (%s, %s, %s)",
                           (student_id, date, status))
            conn.commit()
            cursor.close()
            conn.close()
            QMessageBox.information(window, "Success", "Attendance added.")
            clear_fields()
            refresh_list()
        except mysql.connector.Error as err:
            QMessageBox.critical(window, "Database Error", str(err))

    def delete_attendance():
        record_id = delete_entry.text().strip()
        if not record_id.isdigit():
            QMessageBox.warning(window, "Validation", "Enter valid attendance ID.")
            return
        confirm = QMessageBox.question(window, "Confirm Delete",
                                       f"Delete attendance record {record_id}?",
                                       QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            try:
                conn = mysql.connector.connect(**DB_CONFIG)
                cursor = conn.cursor()
                cursor.execute("DELETE FROM attendance WHERE id = %s", (record_id,))
                conn.commit()
                cursor.close()
                conn.close()
                QMessageBox.information(window, "Deleted", "Attendance deleted.")
                delete_entry.clear()
                refresh_list()
            except mysql.connector.Error as err:
                QMessageBox.critical(window, "Database Error", str(err))

    def update_attendance():
        record_id = delete_entry.text().strip()
        student_id = student_id_entry.text().strip()
        date = date_entry.text().strip()
        status = status_entry.text().strip()

        if not (record_id.isdigit() and student_id and date and status):
            QMessageBox.warning(window, "Validation", "All fields including ID are required.")
            return
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            cursor.execute("UPDATE attendance SET student_id=%s, date=%s, status=%s WHERE id=%s",
                           (student_id, date, status, record_id))
            conn.commit()
            cursor.close()
            conn.close()
            QMessageBox.information(window, "Updated", "Attendance updated.")
            clear_fields()
            refresh_list()
        except mysql.connector.Error as err:
            QMessageBox.critical(window, "Database Error", str(err))

    def clear_fields():
        student_id_entry.clear()
        date_entry.clear()
        status_entry.clear()
        delete_entry.clear()

    # Buttons
    button_layout = QHBoxLayout()
    button_layout.addWidget(styled_btn("Add Attendance", "#27ae60", add_attendance))
    button_layout.addWidget(styled_btn("Update Attendance", "#f39c12", update_attendance))
    button_layout.addWidget(styled_btn("Delete Attendance", "#c0392b", delete_attendance))
    button_layout.addWidget(styled_btn("Clear Attendance", "#7f8c8d", clear_fields))
    button_layout.addWidget(styled_btn("Refresh Attendance", "#2980b9", refresh_list))
    main_layout.addLayout(button_layout)

    # Back
    if main_window:
        def go_back():
            window.close()
            main_window.show()
        main_layout.addWidget(styled_btn("⬅ Back", "#34495e", go_back))

    refresh_list()
    window.show()
    return window
