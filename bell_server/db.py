import sqlite3
import datetime

def create_connection():
    conn = sqlite3.connect('database.db', check_same_thread=False)
    return conn

def get_audio_to_play(conn):
    cur = conn.cursor()
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cur.execute("SELECT * FROM bells WHERE Time == ?", (current_time,))
    rows = cur.fetchall()
    return rows
