import mysql.connector
from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
    QMessageBox, QTableWidget, QTableWidgetItem, QApplication,
    QFormLayout, QFrame, QSizePolicy, QSpacerItem
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

from config import DB_CONFIG

def open_admin_window(username, main_window=None):
    window = QWidget()
    window.setWindowTitle("Admin Management")
    window.setFixedSize(1000, 700)

    screen = QApplication.primaryScreen().geometry()
    center_x = int(screen.width() / 2 - window.width() / 2)
    center_y = int(screen.height() / 2 - window.height() / 2)
    window.setGeometry(center_x, center_y, window.width(), window.height())

    main_layout = QVBoxLayout(window)
    main_layout.setContentsMargins(40, 30, 40, 30)
    main_layout.setSpacing(20)

    title = QLabel(f"👤 Admin Management | Welcome, {username}")
    title.setFont(QFont("Segoe UI", 18, QFont.Bold))
    title.setStyleSheet("color: #FFFFFF;")
    title.setAlignment(Qt.AlignCenter)
    main_layout.addWidget(title)

    form_layout = QFormLayout()
    form_layout.setLabelAlignment(Qt.AlignRight)
    form_layout.setFormAlignment(Qt.AlignHCenter | Qt.AlignTop)

    username_entry = QLineEdit()
    password_entry = QLineEdit()
    password_entry.setEchoMode(QLineEdit.Password)
    
    for field in [username_entry, password_entry]:
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

    username_entry.setPlaceholderText("Enter new admin username")
    password_entry.setPlaceholderText("Enter password")
    form_layout.addRow("Username:", username_entry)
    form_layout.addRow("Password:", password_entry)

    form_frame = QFrame()
    form_frame.setLayout(form_layout)
    main_layout.addWidget(form_frame)

    buttons_layout = QHBoxLayout()
    buttons_layout.setSpacing(15)

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

    admin_table = QTableWidget()
    admin_table.setColumnCount(2)
    admin_table.setHorizontalHeaderLabels(["ID", "Username"])
    admin_table.setFont(QFont("Segoe UI", 10))
    admin_table.setStyleSheet("""
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
    admin_table.setAlternatingRowColors(True)
    admin_table.setEditTriggers(QTableWidget.NoEditTriggers)
    admin_table.setSelectionBehavior(QTableWidget.SelectRows)
    admin_table.horizontalHeader().setStretchLastSection(True)
    main_layout.addWidget(admin_table)

    delete_layout = QHBoxLayout()
    delete_layout.setSpacing(10)
    delete_entry = QLineEdit()
    delete_entry.setPlaceholderText("Admin ID to delete or update")
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
    delete_layout.addWidget(delete_entry)

    def refresh_list():
        admin_table.setRowCount(0)
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            cursor.execute("SELECT id, username FROM admins ORDER BY id ASC")
            rows = cursor.fetchall()
            cursor.close()
            conn.close()
            for row_idx, row in enumerate(rows):
                admin_table.insertRow(row_idx)
                for col_idx, value in enumerate(row):
                    admin_table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))
        except mysql.connector.Error as err:
            QMessageBox.critical(window, "Database Error", str(err))

    def add_admin():
        user = username_entry.text().strip()
        pwd = password_entry.text().strip()
        if not user or not pwd:
            QMessageBox.warning(window, "Validation Error", "Both username and password are required.")
            return
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO admins (username, password) VALUES (%s, %s)", (user, pwd))
            conn.commit()
            cursor.close()
            conn.close()
            QMessageBox.information(window, "Success", "Admin added successfully.")
            username_entry.clear()
            password_entry.clear()
            refresh_list()
        except mysql.connector.Error as err:
            QMessageBox.critical(window, "Database Error", str(err))

    def delete_admin():
        admin_id = delete_entry.text().strip()
        if not admin_id.isdigit():
            QMessageBox.warning(window, "Validation Error", "Please enter a valid numeric Admin ID.")
            return
        confirm = QMessageBox.question(window, "Confirm Delete",
                                       f"Are you sure you want to delete Admin ID {admin_id}?",
                                       QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            try:
                conn = mysql.connector.connect(**DB_CONFIG)
                cursor = conn.cursor()
                cursor.execute("DELETE FROM admins WHERE id = %s", (admin_id,))
                if cursor.rowcount == 0:
                    QMessageBox.information(window, "Not Found", "No admin found with the given ID.")
                else:
                    QMessageBox.information(window, "Success", "Admin deleted successfully.")
                    delete_entry.clear()
                    refresh_list()
                conn.commit()
                cursor.close()
                conn.close()
            except mysql.connector.Error as err:
                QMessageBox.critical(window, "Database Error", str(err))

    def update_admin():
        admin_id = delete_entry.text().strip()
        user = username_entry.text().strip()
        pwd = password_entry.text().strip()
        if not admin_id.isdigit():
            QMessageBox.warning(window, "Validation Error", "Please enter a valid numeric Admin ID to update.")
            return
        if not user or not pwd:
            QMessageBox.warning(window, "Validation Error", "Both username and password are required for update.")
            return
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM admins WHERE id = %s", (admin_id,))
            if cursor.fetchone() is None:
                QMessageBox.information(window, "Not Found", f"No admin found with ID {admin_id}.")
                cursor.close()
                conn.close()
                return
            cursor.execute(
                "UPDATE admins SET username = %s, password = %s WHERE id = %s",
                (user, pwd, admin_id)
            )
            conn.commit()
            cursor.close()
            conn.close()
            QMessageBox.information(window, "Success", "Admin updated successfully.")
            username_entry.clear()
            password_entry.clear()
            delete_entry.clear()
            refresh_list()
        except mysql.connector.Error as err:
            QMessageBox.critical(window, "Database Error", str(err))

    def clear_fields():
        username_entry.clear()
        password_entry.clear()
        delete_entry.clear()

    buttons_layout.addWidget(styled_btn("Add Admin", "#27ae60", add_admin))
    buttons_layout.addWidget(styled_btn("Update Admin", "#f39c12", update_admin))
    buttons_layout.addWidget(styled_btn("Delete Admin", "#c0392b", delete_admin))
    buttons_layout.addWidget(styled_btn("Clear Admin", "#7f8c8d", clear_fields))
    buttons_layout.addWidget(styled_btn("Refresh Admin", "#2980b9", refresh_list))

    main_layout.addLayout(delete_layout)
    main_layout.addLayout(buttons_layout)
    main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

    if main_window:
        def go_back():
            window.close()
            main_window.show()

        back_btn = styled_btn("⬅ Back to Dashboard", "#34495e", go_back)
        main_layout.addWidget(back_btn)

    refresh_list()
    window.show()
    return window
