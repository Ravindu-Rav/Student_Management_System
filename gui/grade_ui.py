import sys
import os
import tkinter as tk
from tkinter import messagebox, font
import mysql.connector

# Adjust path to access config
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config import DB_CONFIG

# --- Fetch Courses from DB ---
def fetch_courses():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SELECT id, course_name FROM courses")
        results = cursor.fetchall()
        conn.close()
        return results
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", str(err))
        return []

# --- CRUD Operations ---
def assign_grade(student_id, course_id, grade):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO grades (student_id, course_id, grade) VALUES (%s, %s, %s)",
                       (student_id, course_id, grade))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Grade assigned successfully.")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", str(err))

def update_grade(grade_id, student_id, course_id, grade):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("UPDATE grades SET student_id = %s, course_id = %s, grade = %s WHERE id = %s",
                       (student_id, course_id, grade, grade_id))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Grade updated successfully.")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", str(err))

def delete_grade(grade_id):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM grades WHERE id = %s", (grade_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Grade deleted successfully.")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", str(err))

def view_grades(listbox):
    listbox.delete(0, tk.END)
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
        conn.close()
        for row in rows:
            listbox.insert(tk.END, f"Grade ID: {row[0]} | {row[1]} | {row[2]} | Grade: {row[3]}")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", str(err))

# --- Main UI ---
def open_grade_window(username, main_window):
    window = tk.Toplevel()
    window.title("Manage Grades")
    window.geometry("800x650")
    window.configure(bg="#f0f0f0")

    header_font = font.Font(family="Helvetica", size=14, weight="bold")
    label_font = font.Font(family="Helvetica", size=11)
    entry_font = font.Font(family="Helvetica", size=11)
    button_font = font.Font(family="Helvetica", size=11, weight="bold")

    tk.Label(window, text=f"Welcome: {username}", fg="blue", bg="#f0f0f0", font=header_font).pack(pady=10)

    form_frame = tk.Frame(window, bg="#f0f0f0")
    form_frame.pack(pady=10)

    # --- Input Fields ---
    tk.Label(form_frame, text="Grade ID (for Update)", font=label_font, bg="#f0f0f0").grid(row=0, column=0, sticky="e", padx=10, pady=5)
    grade_id_entry = tk.Entry(form_frame, font=entry_font, width=30)
    grade_id_entry.grid(row=0, column=1, pady=5)

    tk.Label(form_frame, text="Student ID", font=label_font, bg="#f0f0f0").grid(row=1, column=0, sticky="e", padx=10, pady=5)
    student_entry = tk.Entry(form_frame, font=entry_font, width=30)
    student_entry.grid(row=1, column=1, pady=5)

    # --- Course Dropdown ---
    tk.Label(form_frame, text="Select Course", font=label_font, bg="#f0f0f0").grid(row=2, column=0, sticky="e", padx=10, pady=5)
    courses = fetch_courses()
    course_options = {name: cid for cid, name in courses}
    selected_course_name = tk.StringVar(value=list(course_options.keys())[0] if course_options else "")
    course_dropdown = tk.OptionMenu(form_frame, selected_course_name, *course_options.keys())
    course_dropdown.config(width=28, font=entry_font)
    course_dropdown.grid(row=2, column=1, sticky="w", pady=5)

    # --- Grade Dropdown ---
    tk.Label(form_frame, text="Grade (A-F)", font=label_font, bg="#f0f0f0").grid(row=3, column=0, sticky="e", padx=10, pady=5)
    grade_options = ["A", "B", "C", "D", "E", "F"]
    selected_grade = tk.StringVar(value="A")
    grade_dropdown = tk.OptionMenu(form_frame, selected_grade, *grade_options)
    grade_dropdown.config(width=28, font=entry_font)
    grade_dropdown.grid(row=3, column=1, sticky="w", pady=5)

    tk.Label(form_frame, text="Delete by Grade ID", font=label_font, bg="#f0f0f0").grid(row=4, column=0, sticky="e", padx=10, pady=5)
    delete_entry = tk.Entry(form_frame, font=entry_font, width=30)
    delete_entry.grid(row=4, column=1, pady=5)

    # --- Buttons ---
    button_frame = tk.Frame(window, bg="#f0f0f0")
    button_frame.pack(pady=10)

    tk.Button(button_frame, text="Assign Grade", font=button_font, width=15,
              command=lambda: assign_grade(student_entry.get(), course_options.get(selected_course_name.get()), selected_grade.get())
              ).grid(row=0, column=0, padx=10, pady=5)

    tk.Button(button_frame, text="Update Grade", font=button_font, width=15,
              command=lambda: update_grade(grade_id_entry.get(), student_entry.get(), course_options.get(selected_course_name.get()), selected_grade.get())
              ).grid(row=0, column=1, padx=10, pady=5)

    tk.Button(button_frame, text="Clear Fields", font=button_font, width=15,
              command=lambda: [grade_id_entry.delete(0, tk.END),
                               student_entry.delete(0, tk.END),
                               delete_entry.delete(0, tk.END)]
              ).grid(row=0, column=2, padx=10, pady=5)

    tk.Button(button_frame, text="Delete Grade", font=button_font, width=15,
              command=lambda: delete_grade(delete_entry.get())
              ).grid(row=1, column=0, padx=10, pady=5)

    tk.Button(button_frame, text="Refresh Grades", font=button_font, width=15,
              command=lambda: view_grades(grade_listbox)
              ).grid(row=1, column=1, padx=10, pady=5)

    # --- Listbox ---
    grade_listbox = tk.Listbox(window, width=90, height=10, font=entry_font)
    grade_listbox.pack(pady=20)

    # --- Back Button ---
    def back_to_main():
        window.destroy()
        main_window.deiconify()

    tk.Button(window, text="Back", font=button_font, bg="#d1d1d1", width=20, command=back_to_main).pack(pady=10)

    # Load grades initially
    view_grades(grade_listbox)
