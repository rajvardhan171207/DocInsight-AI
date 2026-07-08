import sqlite3

def create_database():
    conn = sqlite3.connect("docinsight.db")
    cursor = conn.cursor()

    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    # History table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            filename TEXT,
            category TEXT,
            words INTEGER,
            characters INTEGER,
            upload_time TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()

    print("Database Created Successfully!")

if __name__ == "__main__":
    create_database()