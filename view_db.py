import sqlite3

# Create/connect to database
conn = sqlite3.connect('smart_college_assistant.db')
cursor = conn.cursor()

# Create tables
cursor.execute('''CREATE TABLE IF NOT EXISTS block (
    id INTEGER PRIMARY KEY, name TEXT, prefix TEXT, description TEXT, created_at TEXT)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS faculty (
    id INTEGER PRIMARY KEY, name TEXT, department TEXT, designation TEXT, 
    contact TEXT, room_number TEXT, block_id INTEGER, created_at TEXT)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS timetable (
    id INTEGER PRIMARY KEY, department TEXT, day TEXT, subject TEXT, 
    faculty_name TEXT, room_number TEXT, time_slot TEXT, created_at TEXT)''')

# Insert sample data from your original DB
blocks = [
    (1, 'IA Research Park', 'AE', 'Aeronautical Engineering Block', '2025-10-05'),
    (2, 'Mechanical Block', 'ME', 'Mechanical Engineering Block', '2025-10-05')
]
cursor.executemany('INSERT OR REPLACE INTO block VALUES (?,?,?,?,?)', blocks)

faculty = [
    (1, 'sanjay', 'CSE', 'hod', '9999999999', 'ew99', None, '2025-12-23'),
    (2, 'navaneethan', 'ECE', 'maths hod', '7373415129', 'EW210', None, '2025-10-14')
]
cursor.executemany('INSERT OR REPLACE INTO faculty VALUES (?,?,?,?,?,?,?,?)', faculty)

conn.commit()

# Now list tables and data
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print("Tables:", [row[0] for row in cursor.fetchall()])

tables = ['block', 'faculty', 'timetable']
for table in tables:
    print(f"\n=== {table.upper()} ===")
    cursor.execute(f"SELECT * FROM {table}")
    for row in cursor.fetchall():
        print(row)

conn.close()
print("\nDatabase recreated successfully!")
