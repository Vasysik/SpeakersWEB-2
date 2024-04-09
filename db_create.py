import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS bells (
                Id INTEGER PRIMARY KEY,
                Info TEXT,
                Time DATETIME,
                AudioFile TEXT,
                Duration TIMESPAN,
                UploaderName TEXT
            )''')