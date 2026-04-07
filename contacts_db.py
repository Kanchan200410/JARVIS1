import mysql.connector

# Connect to MySQL
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",   # default XAMPP password is empty
        database="jarvis"
    )


# ➕ Add contact
def add_contact(name, number):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO contacts (name, number) VALUES (%s, %s) ON DUPLICATE KEY UPDATE number=%s",
                   (name, number, number))

    conn.commit()
    conn.close()

    return f"Contact {name} saved"


# 🔍 Get contact
def get_contact(name):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT number FROM contacts WHERE name=%s", (name,))
    result = cursor.fetchone()

    conn.close()

    return result[0] if result else None