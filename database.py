import sqlite3

conn = sqlite3.connect("history.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    review TEXT,
    prediction TEXT,
    emotion TEXT
)
""")

print("History table created!")

conn.commit()

conn.close()