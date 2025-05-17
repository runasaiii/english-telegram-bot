import sqlite3
from datetime import datetime

conn = sqlite3.connect("data/history.db")
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS sent_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT NOT NULL,         -- word, task, quiz
        item TEXT NOT NULL,             -- сам текст или уникальный ключ
        sent_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')
conn.commit()

def was_sent(category, item):
    cursor.execute('SELECT 1 FROM sent_items WHERE category = ? AND item = ?', (category, item))
    return cursor.fetchone() is not None

def mark_as_sent(category, item):
    cursor.execute('INSERT INTO sent_items (category, item) VALUES (?, ?)', (category, item))
    conn.commit()
