# main.py

from modules import student, course, grades, attendance, auth

def main_menu():
    while True:
        print("\n--- Student Management System ---")
        print("1. Manage Students")
        print("2. Manage Courses")
        print("3. Manage Grades")
        print("4. Manage Attendance")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            student.student_menu()
        elif choice == "2":
            course.course_menu()
        elif choice == "3":
            grades.grade_menu()
        elif choice == "4":
            attendance.attendance_menu()
        elif choice == "5":
            print("Exiting system.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    if auth.login():
        main_menu()
