from dotenv import load_dotenv
load_dotenv()
import os
import psycopg2

DATABASE_URL = os.environ.get("DATABASE_URL")

def create_database():

    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role VARCHAR(20) DEFAULT 'user'
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history(
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id),
            filename TEXT,
            category TEXT,
            words INTEGER,
            characters INTEGER,
            upload_time TEXT
        );
    """)

    conn.commit()
    cursor.close()
    conn.close()

    print("PostgreSQL Database Created Successfully!")

if __name__ == "__main__":
    create_database()