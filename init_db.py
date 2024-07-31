import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO meetings (subject, date, start_time, end_time, participants) VALUES (?, ?, ?, ?, ?)",
            ('Subject 1', '2024-08-01', '08:00', '09:00', 'Emre Muslu, Emir Muslu')
            )

cur.execute("INSERT INTO meetings (subject, date, start_time, end_time, participants) VALUES (?, ?, ?, ?, ?)",
            ('Subject 2', '2024-08-02', '08:00', '09:00', 'Emre Muslu, Emir Muslu')
            )

connection.commit()
connection.close()