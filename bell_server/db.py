import sqlite3
import datetime

conn = None
conn = sqlite3.connect('database.db')

def get_audio_to_play():
    cur = conn.cursor()
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cur.execute("SELECT * FROM bells WHERE Time == ?", (current_time,))
    rows = cur.fetchall()
    return rows
