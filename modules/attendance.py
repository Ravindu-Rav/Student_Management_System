# modules/attendance.py

import mysql.connector
from gui.config import DB_CONFIG

def attendance_menu():
    while True:
        print("\n--- Attendance Management ---")
        print("1. Mark Attendance")
        print("2. View Attendance")
        print("3. Update Attendance")
        print("4. Delete Attendance")
        print("5. Back to Main Menu")

        choice = input("Enter your choice: ")

        if choice == "1":
            mark_attendance()
        elif choice == "2":
            view_attendance()
        elif choice == "3":
            update_attendance()
        elif choice == "4":
            delete_attendance()
        elif choice == "5":
            break
        else:
            print("Invalid choice.")

def mark_attendance():
    student_id = input("Student ID: ")
    course_id = input("Course ID: ")
    date = input("Date (YYYY-MM-DD): ")
    status = input("Status (Present/Absent): ").capitalize()

    if status not in ["Present", "Absent"]:
        print("Invalid status. Please enter 'Present' or 'Absent'.")
        return

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO attendance (student_id, course_id, date, status)
            VALUES (%s, %s, %s, %s)
        """, (student_id, course_id, date, status))
        conn.commit()
        print("Attendance marked successfully.")
    except mysql.connector.Error as err:
        print("Error:", err)
    finally:
        cursor.close()
        conn.close()

def view_attendance():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        query = """
        SELECT a.id, s.full_name, c.course_name, a.date, a.status
        FROM attendance a
        JOIN students s ON a.student_id = s.id
        JOIN courses c ON a.course_id = c.id
        ORDER BY a.date DESC
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        print("\n--- Attendance Records ---")
        for row in rows:
            print(f"ID: {row[0]}, Student: {row[1]}, Course: {row[2]}, Date: {row[3]}, Status: {row[4]}")
    except mysql.connector.Error as err:
        print("Error:", err)
    finally:
        cursor.close()
        conn.close()

def update_attendance():
    attendance_id = input("Enter Attendance ID to update: ")
    new_status = input("New Status (Present/Absent): ").capitalize()

    if new_status not in ["Present", "Absent"]:
        print("Invalid status.")
        return

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("UPDATE attendance SET status = %s WHERE id = %s", (new_status, attendance_id))
        conn.commit()
        print("Attendance updated successfully.")
    except mysql.connector.Error as err:
        print("Error:", err)
    finally:
        cursor.close()
        conn.close()

def delete_attendance():
    attendance_id = input("Enter Attendance ID to delete: ")

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM attendance WHERE id = %s", (attendance_id,))
        conn.commit()
        print("Attendance record deleted successfully.")
    except mysql.connector.Error as err:
        print("Error:", err)
    finally:
        cursor.close()
        conn.close()
