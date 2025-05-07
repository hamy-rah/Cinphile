import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect("subscriptions.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS subscriptions (
            user_id TEXT PRIMARY KEY,
            subscription_start TEXT
        )
    """)
    conn.commit()
    conn.close()

def add_user(user_id):
    conn = sqlite3.connect("subscriptions.db")
    c = conn.cursor()
    now = datetime.now().isoformat()
    c.execute("INSERT OR IGNORE INTO subscriptions (user_id, subscription_start) VALUES (?, ?)", (user_id, now))
    conn.commit()
    conn.close()

def get_subscription_start(user_id):
    conn = sqlite3.connect("subscriptions.db")
    c = conn.cursor()
    c.execute("SELECT subscription_start FROM subscriptions WHERE user_id = ?", (user_id,))
    row = c.fetchone()
    conn.close()
    if row:
        return datetime.fromisoformat(row[0])
    return None
