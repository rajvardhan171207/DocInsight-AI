from db import get_connection

conn = get_connection()
cursor = conn.cursor()

cursor.execute("SELECT * FROM history")

rows = cursor.fetchall()

for row in rows:
    print(dict(row))

conn.close()
