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

def seconds_to_hms(seconds):
    minutes, seconds = divmod(int(seconds), 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

def add_bell(info, time, audio_file, duration, uploader_name):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute('''INSERT INTO bells (Info, Time, AudioFile, Duration, UploaderName)
                 VALUES (?, ?, ?, ?, ?)''',
              (info, time, audio_file, seconds_to_hms(duration), uploader_name))

    conn.commit()
    conn.close()

def get_all_bells():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute('SELECT * FROM bells ORDER BY Time ASC')
    bells = [
        {
            'id': row[0],
            'info': row[1],
            'time': row[2],
            'audioFile': row[3],
            'duration': row[4],
            'uploaderName': row[5]
        } for row in c.fetchall()
    ]

    conn.close()
    return bells

def get_user(username):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute('SELECT * FROM users WHERE username=?', (username,))
    user = c.fetchone()

    conn.close()
    if user:
        return {'id': user[0], 'username': user[1], 'password': user[2]}
    else:
        return None