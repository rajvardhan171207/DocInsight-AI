import sqlite3

conn = sqlite3.connect("docinsight.db")
cursor = conn.cursor()

try:
    cursor.execute("""
        ALTER TABLE users
        ADD COLUMN role TEXT DEFAULT 'user'
    """)
    print("Role column added.")
except:
    print("Role column already exists.")

cursor.execute("""
UPDATE users
SET role='admin'
WHERE email='rajvardhansinghrathod07@gmail.com'
""")

conn.commit()
conn.close()

print("Done")