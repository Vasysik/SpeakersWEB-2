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

c.execute('''CREATE TABLE IF NOT EXISTS users (
                Id INTEGER PRIMARY KEY,
                Username TEXT,
                Password TEXT
            );''')

conn.commit()

c.execute("SELECT COUNT(*) FROM users")
count = c.fetchone()[0]

if count == 0:
    c.execute('''INSERT INTO users (Username, Password) VALUES ('test_user', 'test_password')''')
    conn.commit()

conn.close()