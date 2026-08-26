import sqlite3

DB_NAME = "subscriptions.db"


def init_db():

    conn = sqlite3.connect(DB_NAME)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS subscriptions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id TEXT NOT NULL,
        payment_id TEXT UNIQUE,
        subscription_id TEXT,
        plan_type TEXT,
        start_date TEXT,
        end_date TEXT,
        status TEXT
    )
    """)

    conn.commit()
    conn.close()
    
