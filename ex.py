import sqlite3

conn = sqlite3.connect("civic_ai.db")
cursor = conn.cursor()

cursor.execute("DELETE FROM issues")

conn.commit()
conn.close()

print("All issues deleted")

