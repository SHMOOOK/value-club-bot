import sqlite3

conn = sqlite3.connect("subscriptions.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    telegram_id INTEGER,
    plan TEXT,
    status TEXT
)
""")

conn.commit()
conn.close()
