from PySide6.QtWidgets import (
    QWidget, QLabel, QComboBox, QPushButton, QVBoxLayout, QHBoxLayout, QFormLayout,
    QMessageBox, QApplication, QLineEdit, QFrame, QTableWidget, QTableWidgetItem
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
import mysql.connector

from config import DB_CONFIG


def open_grade_window(admin_id,username, main_window=None):
    window = QWidget()
    window.setWindowTitle("Manage Grades")
    window.setFixedSize(1000, 700)

    screen = QApplication.primaryScreen().geometry()
    center_x = int(screen.width() / 2 - window.width() / 2)
    center_y = int(screen.height() / 2 - window.height() / 2)
    window.setGeometry(center_x, center_y, 1000, 700)

    main_layout = QVBoxLayout(window)
    main_layout.setContentsMargins(40, 30, 40, 30)
    main_layout.setSpacing(20)

    title = QLabel(f"🎓 Manage Grades | Welcome, {username}")
    title.setFont(QFont("Segoe UI", 18, QFont.Bold))
    title.setAlignment(Qt.AlignCenter)
    title.setStyleSheet("color: #FFFFFF;")
    main_layout.addWidget(title)

    # --- Form Section ---
    form_layout = QFormLayout()
    form_layout.setLabelAlignment(Qt.AlignRight)

    student_combo = QComboBox()
    course_combo = QComboBox()
    grade_input = QLineEdit()

    grade_input.setPlaceholderText("Enter Grade (e.g. A, B+, 90)")

    for widget in (student_combo, course_combo, grade_input):
        widget.setFont(QFont("Segoe UI", 11))

    input_style = """
        QComboBox, QLineEdit {
            padding: 8px;
            border: 2px solid #bdc3c7;
            border-radius: 10px;
        }
        QComboBox:focus, QLineEdit:focus {
            border-color: #3498db;
        }
    """
    student_combo.setStyleSheet(input_style)
    course_combo.setStyleSheet(input_style)
    grade_input.setStyleSheet(input_style)

    form_layout.addRow("Student:", student_combo)
    form_layout.addRow("Course:", course_combo)
    form_layout.addRow("Grade:", grade_input)

    form_frame = QFrame()
    form_frame.setLayout(form_layout)
    main_layout.addWidget(form_frame)

    # --- Grade Table ---
    grade_table = QTableWidget()
    grade_table.setColumnCount(4)
    grade_table.setHorizontalHeaderLabels(["ID", "Student", "Course", "Grade"])
    grade_table.setEditTriggers(QTableWidget.NoEditTriggers)
    grade_table.setSelectionBehavior(QTableWidget.SelectRows)
    grade_table.setStyleSheet("""
        QTableWidget {
            border: 1px solid #bdc3c7;
            border-radius: 10px;
            background-color: #ffffff;
            color: #2c3e50;
            gridline-color: #bdc3c7;
        }
        QHeaderView::section {
            background-color: #3498db;
             color: #2c3e50;
            padding: 6px;
            font-weight: bold;
        }
    """)
    grade_table.setFont(QFont("Segoe UI", 10))
    grade_table.horizontalHeader().setStretchLastSection(True)
    grade_table.setAlternatingRowColors(True)
    main_layout.addWidget(grade_table)

    delete_id_input = QLineEdit()
    delete_id_input.setPlaceholderText("Grade ID to delete or update")
    delete_id_input.setFont(QFont("Segoe UI", 11))
    delete_id_input.setStyleSheet("""
        QLineEdit {
            padding: 8px;
            border: 2px solid #bdc3c7;
            border-radius: 10px;
        }
        QLineEdit:focus {
            border-color: #c0392b;
        }
    """)
    main_layout.addWidget(delete_id_input)

    # --- Populate student and course combos ---
    def populate_dropdowns():
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            cursor.execute("SELECT id, full_name FROM students ORDER BY full_name")
            student_combo.clear()
            for sid, sname in cursor.fetchall():
                student_combo.addItem(sname, sid)

            cursor.execute("SELECT id, course_name FROM courses ORDER BY course_name")
            course_combo.clear()
            for cid, cname in cursor.fetchall():
                course_combo.addItem(cname, cid)

            cursor.close()
            conn.close()
        except mysql.connector.Error as err:
            QMessageBox.critical(window, "Database Error", str(err))

    populate_dropdowns()

    def clear_inputs():
        student_combo.setCurrentIndex(0)
        course_combo.setCurrentIndex(0)
        grade_input.clear()
        delete_id_input.clear()

    def refresh_grade_table():
        grade_table.setRowCount(0)
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT g.id, s.full_name, c.course_name, g.grade
                FROM grades g
                JOIN students s ON g.student_id = s.id
                JOIN courses c ON g.course_id = c.id
                ORDER BY s.full_name, c.course_name
            """)
            rows = cursor.fetchall()
            grade_table.setRowCount(len(rows))
            for i, (gid, student, course, grade) in enumerate(rows):
                grade_table.setItem(i, 0, QTableWidgetItem(str(gid)))
                grade_table.setItem(i, 1, QTableWidgetItem(student))
                grade_table.setItem(i, 2, QTableWidgetItem(course))
                grade_table.setItem(i, 3, QTableWidgetItem(grade))
            cursor.close()
            conn.close()
        except mysql.connector.Error as err:
            QMessageBox.critical(window, "Database Error", str(err))

    def add_grade():
        sid = student_combo.currentData()
        cid = course_combo.currentData()
        grade_val = grade_input.text().strip()

        if not sid or not cid or not grade_val:
            QMessageBox.warning(window, "Validation", "All fields are required.")
            return

        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO grades (student_id, course_id, grade, admin_id) VALUES (%s, %s, %s, %s)",
                           (sid, cid, grade_val, admin_id))
            conn.commit()
            cursor.close()
            conn.close()
            QMessageBox.information(window, "Success", "Grade added.")
            clear_inputs()
            refresh_grade_table()
        except mysql.connector.Error as err:
            QMessageBox.critical(window, "Database Error", str(err))

    def delete_grade():
        gid = delete_id_input.text().strip()
        if not gid.isdigit():
            QMessageBox.warning(window, "Validation", "Enter valid Grade ID.")
            return

        confirm = QMessageBox.question(window, "Confirm Delete",
                                       f"Delete grade ID {gid}?",
                                       QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            try:
                conn = mysql.connector.connect(**DB_CONFIG)
                cursor = conn.cursor()
                cursor.execute("DELETE FROM grades WHERE id = %s", (gid,))
                if cursor.rowcount == 0:
                    QMessageBox.information(window, "Info", "Grade not found.")
                else:
                    QMessageBox.information(window, "Success", "Grade deleted.")
                    clear_inputs()
                    refresh_grade_table()
                conn.commit()
                cursor.close()
                conn.close()
            except mysql.connector.Error as err:
                QMessageBox.critical(window, "Database Error", str(err))

    def update_grade():
        gid = delete_id_input.text().strip()
        if not gid.isdigit():
            QMessageBox.warning(window, "Validation", "Enter valid Grade ID.")
            return

        sid = student_combo.currentData()
        cid = course_combo.currentData()
        grade_val = grade_input.text().strip()

        if not sid or not cid or not grade_val:
            QMessageBox.warning(window, "Validation", "All fields are required.")
            return

        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM grades WHERE id = %s", (gid,))
            if not cursor.fetchone():
                QMessageBox.warning(window, "Not Found", "Grade ID does not exist.")
                return

            cursor.execute("""
                UPDATE grades
                SET student_id = %s, course_id = %s, grade = %s
                WHERE id = %s
            """, (sid, cid, grade_val, gid))
            conn.commit()
            cursor.close()
            conn.close()
            QMessageBox.information(window, "Success", "Grade updated.")
            clear_inputs()
            refresh_grade_table()
        except mysql.connector.Error as err:
            QMessageBox.critical(window, "Database Error", str(err))

    # --- Buttons ---
    button_layout = QHBoxLayout()
    button_layout.setSpacing(15)

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

    button_layout.addWidget(styled_btn("Add Grade", add_grade, "#27ae60"))
    button_layout.addWidget(styled_btn("Update Grade", update_grade, "#f39c12"))
    button_layout.addWidget(styled_btn("Delete Grade", delete_grade, "#c0392b"))
    button_layout.addWidget(styled_btn("Refresh Grade", refresh_grade_table, "#2980b9"))
    button_layout.addWidget(styled_btn("Clear Grade", clear_inputs, "#7f8c8d"))

    main_layout.addLayout(button_layout)

    # Back button
    if main_window:
        def go_back():
            window.close()
            main_window.show()
        back_btn = styled_btn("⬅ Back to Dashboard", go_back, "#34495e")
        main_layout.addWidget(back_btn)

    refresh_grade_table()
    window.show()
    return window
