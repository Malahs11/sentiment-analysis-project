import sqlite3

conn = sqlite3.connect("history.db")

cursor = conn.cursor()

cursor.execute("""

CREATE TABLE IF NOT EXISTS history (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    review TEXT,

    prediction TEXT,

    emotion TEXT

)

""")

conn.commit()

conn.close()

print("Database Created Successfully")