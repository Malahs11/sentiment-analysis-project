import sqlite3

# Connect database
conn = sqlite3.connect("history.db")

cursor = conn.cursor()

# Read data
cursor.execute("SELECT * FROM history")

rows = cursor.fetchall()

# Print rows
for row in rows:
    print(row)

# Close connection
conn.close()