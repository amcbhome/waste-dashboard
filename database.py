import sqlite3

DB_PATH = "data/waste.db"

def get_upcoming_collections(limit=10):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    SELECT date, type
    FROM collections
    ORDER BY date ASC
    LIMIT ?
    """, (limit,))

    rows = cur.fetchall()
    conn.close()

    return rows
