# modules/auth.py

import mysql.connector
from config import DB_CONFIG

def login():
    print("Admin Login")
    username = input("Username: ")
    password = input("Password: ")

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        query = "SELECT * FROM admins WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        result = cursor.fetchone()

        cursor.close()
        conn.close()

        if result:
            print("Login successful!\n")
            return True
        else:
            print("Login failed! Invalid username or password.\n")
            return False

    except mysql.connector.Error as err:
        print("Database Error:", err)
        return False
