from db import get_connection

conn = get_connection()
cursor = conn.cursor()

print("===== USERS =====")
cursor.execute("SELECT * FROM users")
for row in cursor.fetchall():
    print(dict(row))

print("\n===== HISTORY =====")
cursor.execute("SELECT * FROM history")
for row in cursor.fetchall():
    print(dict(row))

conn.close()
#python view_database.py