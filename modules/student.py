# modules/student.py

import mysql.connector
from gui.config import DB_CONFIG

def student_menu():
    while True:
        print("\n--- Student Management ---")
        print("1. Add Student")
        print("2. View All Students")
        print("3. Update Student")
        print("4. Delete Student")
        print("5. Back to Main Menu")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_student()
        elif choice == "2":
            view_students()
        elif choice == "3":
            update_student()
        elif choice == "4":
            delete_student()
        elif choice == "5":
            break
        else:
            print("Invalid choice.")

def add_student():
    name = input("Full Name: ")
    email = input("Email: ")
    phone = input("Phone: ")
    enrollment_date = input("Enrollment Date (YYYY-MM-DD): ")

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO students (full_name, email, phone, enrollment_date) VALUES (%s, %s, %s, %s)",
                       (name, email, phone, enrollment_date))
        conn.commit()
        print("Student added successfully.")
    except mysql.connector.Error as err:
        print("Error:", err)
    finally:
        cursor.close()
        conn.close()

def view_students():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students")
        rows = cursor.fetchall()
        print("\n--- Student List ---")
        for row in rows:
            print(f"ID: {row[0]}, Name: {row[1]}, Email: {row[2]}, Phone: {row[3]}, Enrolled: {row[4]}")
    except mysql.connector.Error as err:
        print("Error:", err)
    finally:
        cursor.close()
        conn.close()

def update_student():
    student_id = input("Enter Student ID to update: ")
    name = input("New Name: ")
    email = input("New Email: ")
    phone = input("New Phone: ")

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("UPDATE students SET full_name=%s, email=%s, phone=%s WHERE id=%s",
                       (name, email, phone, student_id))
        conn.commit()
        print("Student updated successfully.")
    except mysql.connector.Error as err:
        print("Error:", err)
    finally:
        cursor.close()
        conn.close()

def delete_student():
    student_id = input("Enter Student ID to delete: ")

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM students WHERE id = %s", (student_id,))
        conn.commit()
        print("Student deleted successfully.")
    except mysql.connector.Error as err:
        print("Error:", err)
    finally:
        cursor.close()
        conn.close()
