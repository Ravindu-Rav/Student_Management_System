import mysql.connector
from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QFormLayout,
    QMessageBox, QTableWidget, QTableWidgetItem, QApplication
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

from config import DB_CONFIG

def open_course_window(username, main_window=None):
    window = QWidget()
    window.setWindowTitle("Manage Courses")
    window.setFixedSize(1000, 700)

    screen = QApplication.primaryScreen().geometry()
    center_x = int(screen.width() / 2 - window.width() / 2)
    center_y = int(screen.height() / 2 - window.height() / 2)
    window.setGeometry(center_x, center_y, 1000, 700)

    main_layout = QVBoxLayout(window)
    main_layout.setContentsMargins(40, 30, 40, 30)
    main_layout.setSpacing(20)

    title = QLabel(f"📚 Manage Courses | Welcome, {username}")
    title.setFont(QFont("Segoe UI", 18, QFont.Bold))
    title.setStyleSheet("color: #FFFFFF;")
    title.setAlignment(Qt.AlignCenter)
    main_layout.addWidget(title)

    # --- Form Section ---
    form_layout = QFormLayout()
    form_layout.setLabelAlignment(Qt.AlignRight)

    id_input = QLineEdit()
    name_input = QLineEdit()
    desc_input = QLineEdit()

    id_input.setPlaceholderText("Enter Course ID for Update/Delete")
    name_input.setPlaceholderText("Enter Course Name")
    desc_input.setPlaceholderText("Enter Course Description")

    inputs_font = QFont("Segoe UI", 11)
    for inp in (id_input, name_input, desc_input):
        inp.setFont(inputs_font)

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
    id_input.setStyleSheet(input_style)
    name_input.setStyleSheet(input_style)
    desc_input.setStyleSheet(input_style)

    form_layout.addRow("Course ID (for Update/Delete):", id_input)
    form_layout.addRow("Course Name:", name_input)
    form_layout.addRow("Description:", desc_input)

    main_layout.addLayout(form_layout)

    # --- Course Table ---
    course_table = QTableWidget()
    course_table.setColumnCount(3)
    course_table.setHorizontalHeaderLabels(["ID", "Course Name", "Description"])
    course_table.horizontalHeader().setStretchLastSection(True)
    course_table.setEditTriggers(QTableWidget.NoEditTriggers)
    course_table.setSelectionBehavior(QTableWidget.SelectRows)
    course_table.setFont(QFont("Segoe UI", 10))
    course_table.setStyleSheet("""
        QTableWidget {
            border: 1px solid #bdc3c7;
            border-radius: 10px;
            background-color: #f9f9f9;
            color: #2c3e50;
        }
        QHeaderView::section {
            background-color: #2980b9;
            color: #2c3e50;
            font-weight: bold;
            padding: 4px;
        }
    """)
    main_layout.addWidget(course_table)

    # --- Functions ---

    def clear_inputs():
        id_input.clear()
        name_input.clear()
        desc_input.clear()

    def refresh_course_list():
        course_table.setRowCount(0)
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            cursor.execute("SELECT id, course_name, description FROM courses ORDER BY id")
            rows = cursor.fetchall()
            course_table.setRowCount(len(rows))
            for row_idx, row_data in enumerate(rows):
                for col_idx, value in enumerate(row_data):
                    item = QTableWidgetItem(str(value))
                    course_table.setItem(row_idx, col_idx, item)
            cursor.close()
            conn.close()
        except mysql.connector.Error as err:
            QMessageBox.critical(window, "Database Error", str(err))

    def add_course():
        name = name_input.text().strip()
        desc = desc_input.text().strip()
        if not name or not desc:
            QMessageBox.warning(window, "Validation Error", "Course name and description are required.")
            return
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO courses (course_name, description) VALUES (%s, %s)", (name, desc))
            conn.commit()
            cursor.close()
            conn.close()
            QMessageBox.information(window, "Success", "Course added successfully.")
            clear_inputs()
            refresh_course_list()
        except mysql.connector.Error as err:
            QMessageBox.critical(window, "Database Error", str(err))

    def update_course():
        cid = id_input.text().strip()
        if not cid.isdigit():
            QMessageBox.warning(window, "Validation Error", "Enter a valid numeric Course ID.")
            return
        name = name_input.text().strip()
        desc = desc_input.text().strip()
        if not name and not desc:
            QMessageBox.warning(window, "Validation Error", "Enter new name or description to update.")
            return
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            cursor.execute("SELECT course_name, description FROM courses WHERE id = %s", (cid,))
            existing = cursor.fetchone()
            if not existing:
                QMessageBox.critical(window, "Error", "Course ID not found.")
                cursor.close()
                conn.close()
                return
            new_name = name if name else existing[0]
            new_desc = desc if desc else existing[1]
            cursor.execute("UPDATE courses SET course_name = %s, description = %s WHERE id = %s",
                           (new_name, new_desc, cid))
            conn.commit()
            cursor.close()
            conn.close()
            QMessageBox.information(window, "Success", "Course updated successfully.")
            clear_inputs()
            refresh_course_list()
        except mysql.connector.Error as err:
            QMessageBox.critical(window, "Database Error", str(err))

    def delete_course():
        cid = id_input.text().strip()
        if not cid.isdigit():
            QMessageBox.warning(window, "Validation Error", "Enter a valid numeric Course ID.")
            return
        confirm = QMessageBox.question(window, "Confirm Delete",
                                       f"Are you sure you want to delete Course ID {cid}?",
                                       QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            try:
                conn = mysql.connector.connect(**DB_CONFIG)
                cursor = conn.cursor()
                cursor.execute("DELETE FROM courses WHERE id = %s", (cid,))
                if cursor.rowcount == 0:
                    QMessageBox.information(window, "Info", "No such course found.")
                else:
                    QMessageBox.information(window, "Success", "Course deleted successfully.")
                    clear_inputs()
                    refresh_course_list()
                conn.commit()
                cursor.close()
                conn.close()
            except mysql.connector.Error as err:
                QMessageBox.critical(window, "Database Error", str(err))

    # --- Buttons ---
    btn_layout = QHBoxLayout()
    btn_layout.setSpacing(15)

    def styled_btn(text, handler, color="#3498db"):
        btn = QPushButton(text)
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

    btn_layout.addWidget(styled_btn("Add Course", add_course, "#27ae60"))
    btn_layout.addWidget(styled_btn("Update Course", update_course, "#f39c12"))
    btn_layout.addWidget(styled_btn("Delete Course", delete_course, "#c0392b"))
    btn_layout.addWidget(styled_btn("Refresh Course", refresh_course_list, "#2980b9"))
    btn_layout.addWidget(styled_btn("Clear Course", clear_inputs, "#7f8c8d"))

    main_layout.addLayout(btn_layout)

    # --- Back Button ---
    if main_window:
        def go_back():
            window.close()
            main_window.show()

        back_btn = styled_btn("⬅ Back to Dashboard", go_back, "#34495e")
        main_layout.addWidget(back_btn)

    refresh_course_list()
    window.show()
    return window