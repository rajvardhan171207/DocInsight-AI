from db import get_connection
from datetime import datetime


def save_history_db(user_id, filename, category, stats):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO history
        (user_id, filename, category, words, characters, upload_time)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        filename,
        category,
        stats["words"],
        stats["characters"],
        datetime.now().strftime("%d-%m-%Y %I:%M %p")
    ))

    conn.commit()
    print("History Saved Successfully")
    print(user_id, filename)
    conn.close()


def load_history_db(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT filename,
               category,
               words,
               characters,
               upload_time
        FROM history
        WHERE user_id = ?
        ORDER BY id DESC
    """, (user_id,))

    records = cursor.fetchall()

    conn.close()

    return records
def get_dashboard_stats(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            COUNT(*) AS total,
            SUM(CASE WHEN filename LIKE '%.pdf' THEN 1 ELSE 0 END) AS pdf,
            SUM(CASE WHEN filename LIKE '%.docx' THEN 1 ELSE 0 END) AS docx,
            SUM(CASE WHEN filename LIKE '%.txt' THEN 1 ELSE 0 END) AS txt
        FROM history
        WHERE user_id = ?
    """, (user_id,))

    data = cursor.fetchone()

    conn.close()

    return {
        "total": data["total"] or 0,
        "pdf": data["pdf"] or 0,
        "docx": data["docx"] or 0,
        "txt": data["txt"] or 0
    }