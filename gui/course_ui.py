import sys
import os
import tkinter as tk
from tkinter import messagebox, font
import mysql.connector
from config import DB_CONFIG

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def add_course(name, description):
    if not name.strip() or not description.strip():
        messagebox.showwarning("Validation Error", "Course name and description are required.")
        return
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO courses (course_name, description) VALUES (%s, %s)", (name, description))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Course added successfully.")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", str(err))

def update_course(course_id, name, description):
    if not course_id.strip().isdigit():
        messagebox.showwarning("Validation Error", "Enter a valid numeric Course ID.")
        return
    if not name.strip() and not description.strip():
        messagebox.showwarning("Validation Error", "Enter a new name or description to update.")
        return
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        cursor.execute("SELECT course_name, description FROM courses WHERE id = %s", (course_id,))
        existing = cursor.fetchone()
        if not existing:
            messagebox.showerror("Error", "Course ID not found.")
            conn.close()
            return

        new_name = name.strip() if name.strip() else existing[0]
        new_desc = description.strip() if description.strip() else existing[1]

        cursor.execute("UPDATE courses SET course_name = %s, description = %s WHERE id = %s",
                       (new_name, new_desc, course_id))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Course updated successfully.")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", str(err))

def delete_course(course_id):
    if not course_id.strip().isdigit():
        messagebox.showwarning("Validation Error", "Enter a valid numeric Course ID.")
        return
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM courses WHERE id = %s", (course_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Course deleted successfully.")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", str(err))

def view_courses(listbox):
    listbox.delete(0, tk.END)
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM courses")
        rows = cursor.fetchall()
        conn.close()
        for row in rows:
            listbox.insert(tk.END, f"ID: {row[0]} | {row[1]} | {row[2]}")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", str(err))

def center_window(win, width, height):
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    win.geometry(f"{width}x{height}+{x}+{y}")

def open_course_window(username, main_window):
    window = tk.Toplevel()
    window.title("Manage Courses")
    window.resizable(True, True)

    width, height = 1000, 700
    center_window(window, width, height)

    header_font = font.Font(family="Helvetica", size=14, weight="bold")
    label_font = font.Font(family="Helvetica", size=11)
    entry_font = font.Font(family="Helvetica", size=11)

    tk.Label(window, text=f"Welcome: {username}", fg="blue", font=header_font).grid(row=0, column=0, columnspan=2, pady=12)

    # Form fields
    tk.Label(window, text="Course ID (for Update)", font=label_font).grid(row=1, column=0, sticky="e", padx=10, pady=5)
    id_entry = tk.Entry(window, width=10, font=entry_font)
    id_entry.grid(row=1, column=1, sticky="w", pady=5)

    tk.Label(window, text="Course Name", font=label_font).grid(row=2, column=0, sticky="e", padx=10, pady=5)
    name_entry = tk.Entry(window, width=35, font=entry_font)
    name_entry.grid(row=2, column=1, sticky="w", pady=5)

    tk.Label(window, text="Description", font=label_font).grid(row=3, column=0, sticky="e", padx=10, pady=5)
    desc_entry = tk.Entry(window, width=35, font=entry_font)
    desc_entry.grid(row=3, column=1, sticky="w", pady=5)

    # Buttons
    tk.Button(window, text="Add Course", font=label_font,
              command=lambda: add_course(name_entry.get(), desc_entry.get())).grid(row=4, column=1, sticky="w", pady=10)

    tk.Button(window, text="Update Course", font=label_font,
              command=lambda: update_course(id_entry.get(), name_entry.get(), desc_entry.get())).grid(row=5, column=1, sticky="w", pady=5)

    # Listbox
    tk.Label(window, text="Course List", font=label_font).grid(row=6, column=0, columnspan=2, pady=(10, 5))
    course_listbox = tk.Listbox(window, width=90, height=10, font=entry_font)
    course_listbox.grid(row=7, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")

    tk.Button(window, text="Refresh Course List", font=label_font,
              command=lambda: view_courses(course_listbox)).grid(row=8, column=0, columnspan=2, pady=6)

    # Delete
    tk.Label(window, text="Delete by ID", font=label_font).grid(row=9, column=0, sticky="e", padx=10, pady=5)
    delete_entry = tk.Entry(window, font=entry_font)
    delete_entry.grid(row=9, column=1, sticky="w", pady=5)

    tk.Button(window, text="Delete Course", font=label_font,
              command=lambda: delete_course(delete_entry.get())).grid(row=10, column=1, sticky="w", pady=10)

    # Back Button
    def back_to_main():
        window.destroy()
        main_window.deiconify()

    tk.Button(window, text="Back to Main", font=label_font, command=back_to_main).grid(row=11, column=1, sticky="w", pady=15)

    window.protocol("WM_DELETE_WINDOW", back_to_main)

    window.grid_rowconfigure(7, weight=1)
    window.grid_columnconfigure(1, weight=1)

    view_courses(course_listbox)
