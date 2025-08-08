# 🎓 Student Management System

This is a simple **Student Management System** built using **Python** and **MySQL**. The system provides full **CRUD (Create, Read, Update, Delete)** functionality to manage students, courses, grades, and attendance.

## 📌 Features

- 🔐 Admin Login
- 👨‍🎓 Manage Students (add/view/edit/delete)
- 📚 Manage Courses
- 📝 Manage Grades
- 📅 Attendance Tracking
- 🔍 Search Students
- 📊 View Reports (GPA, attendance summary)
- 💾 MySQL Database Integration

---

## 💻 Technologies Used

- **Language**: Python 3.x
- **Database**: MySQL
- **Library**: `mysql-connector-python`

---

## ✅ Prerequisites (Only for First-Time Setup or Development)

Before running the system, ensure the following are installed on your machine:

### 1. MySQL Server
- Required to manage and store all student-related data.
- You can use tools like **XAMPP**, **WAMP**, or install **MySQL Community Server** directly.

### 2. Python 3.x (optional, only if running from source)
- If you plan to run the `.py` files directly (not the `.exe`), install Python 3.10 or later.
- Required Python packages (install with `pip install`):

```bash
pip install PySide6 mysql-connector-python
```

---

## 🚀 How to Run the System

### 🔹 If you're using the pre-built executable:

1. **Locate the Executable:**
   - Go to the `dist` folder in the project directory.
   - Find and double-click the file:  
     **`login_ui.exe`**

2. **Ensure MySQL is Running:**
   - Make sure your MySQL server is active.
   - The system expects a database named `student_db` with appropriate tables.

3. **Login to the System:**
   - Use default credentials (unless changed):

```
Username: admin
Password: admin123
```

4. **System Modules Available:**
   - ✅ Student Management  
   - ✅ Course & Grade Records  
   - ✅ Attendance Management  
   - ✅ Admin Panel

---

## 📄 Notes

- No need for Python or VS Code to run the `.exe` version.
- The `.exe` version is portable and can run on any Windows machine with MySQL configured.
- Database configuration (host, user, password) is stored in `config.py` during development and bundled into the executable.

---

## 📂 Project Folder Structure

```
Student_Management_System/
├── gui/
│   ├── login_ui.py
│   ├── main_ui.py
│   ├── student_ui.py
│   ├── course_ui.py
│   └── attendance_ui.py
├── config.py
├── dist/
│   └── login_ui.exe
└── README.md
```

---

## 📌 Developed With

- Python 3.x
- PySide6
- MySQL / XAMPP
- VS Code

---

