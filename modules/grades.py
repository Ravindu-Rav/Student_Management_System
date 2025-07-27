# modules/grades.py

import mysql.connector
from config import DB_CONFIG

def grade_menu():
    while True:
        print("\n--- Grade Management ---")
        print("1. Assign Grade")
        print("2. View All Grades")
        print("3. Update Grade")
        print("4. Delete Grade")
        print("5. Back to Main Menu")

        choice = input("Enter your choice: ")

        if choice == "1":
            assign_grade()
        elif choice == "2":
            view_grades()
        elif choice == "3":
            update_grade()
        elif choice == "4":
            delete_grade()
        elif choice == "5":
            break
        else:
            print("Invalid choice.")

def assign_grade():
    student_id = input("Student ID: ")
    course_id = input("Course ID: ")
    grade = input("Grade (A-F): ").upper()

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO grades (student_id, course_id, grade) VALUES (%s, %s, %s)",
                       (student_id, course_id, grade))
        conn.commit()
        print("Grade assigned successfully.")
    except mysql.connector.Error as err:
        print("Error:", err)
    finally:
        cursor.close()
        conn.close()

def view_grades():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        query = """
        SELECT g.id, s.full_name, c.course_name, g.grade
        FROM grades g
        JOIN students s ON g.student_id = s.id
        JOIN courses c ON g.course_id = c.id
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        print("\n--- Grades List ---")
        for row in rows:
            print(f"ID: {row[0]}, Student: {row[1]}, Course: {row[2]}, Grade: {row[3]}")
    except mysql.connector.Error as err:
        print("Error:", err)
    finally:
        cursor.close()
        conn.close()

def update_grade():
    grade_id = input("Enter Grade ID to update: ")
    new_grade = input("New Grade (A-F): ").upper()

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("UPDATE grades SET grade = %s WHERE id = %s", (new_grade, grade_id))
        conn.commit()
        print("Grade updated successfully.")
    except mysql.connector.Error as err:
        print("Error:", err)
    finally:
        cursor.close()
        conn.close()

def delete_grade():
    grade_id = input("Enter Grade ID to delete: ")

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM grades WHERE id = %s", (grade_id,))
        conn.commit()
        print("Grade deleted successfully.")
    except mysql.connector.Error as err:
        print("Error:", err)
    finally:
        cursor.close()
        conn.close()
