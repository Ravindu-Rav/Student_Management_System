# modules/course.py

import mysql.connector
from config import DB_CONFIG

def course_menu():
    while True:
        print("\n--- Course Management ---")
        print("1. Add Course")
        print("2. View All Courses")
        print("3. Update Course")
        print("4. Delete Course")
        print("5. Back to Main Menu")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_course()
        elif choice == "2":
            view_courses()
        elif choice == "3":
            update_course()
        elif choice == "4":
            delete_course()
        elif choice == "5":
            break
        else:
            print("Invalid choice.")

def add_course():
    name = input("Course Name: ")
    desc = input("Description: ")

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO courses (course_name, description) VALUES (%s, %s)", (name, desc))
        conn.commit()
        print("Course added successfully.")
    except mysql.connector.Error as err:
        print("Error:", err)
    finally:
        cursor.close()
        conn.close()

def view_courses():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM courses")
        rows = cursor.fetchall()
        print("\n--- Course List ---")
        for row in rows:
            print(f"ID: {row[0]}, Name: {row[1]}, Description: {row[2]}")
    except mysql.connector.Error as err:
        print("Error:", err)
    finally:
        cursor.close()
        conn.close()

def update_course():
    course_id = input("Enter Course ID to update: ")
    name = input("New Course Name: ")
    desc = input("New Description: ")

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("UPDATE courses SET course_name=%s, description=%s WHERE id=%s",
                       (name, desc, course_id))
        conn.commit()
        print("Course updated successfully.")
    except mysql.connector.Error as err:
        print("Error:", err)
    finally:
        cursor.close()
        conn.close()

def delete_course():
    course_id = input("Enter Course ID to delete: ")

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM courses WHERE id = %s", (course_id,))
        conn.commit()
        print("Course deleted successfully.")
    except mysql.connector.Error as err:
        print("Error:", err)
    finally:
        cursor.close()
        conn.close()
