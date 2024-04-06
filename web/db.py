import sqlite3

# Создаем соединение с базой данных
conn = sqlite3.connect('database.db')
c = conn.cursor()

# Создаем таблицу для хранения значения дивергенции
c.execute('''CREATE TABLE IF NOT EXISTS bells (
                id INTEGER PRIMARY KEY,
                value REAL
            )''')

# Сохраняем изменения и закрываем соединение
conn.commit()
conn.close()

# Функция для получения текущего значения дивергенции
def get_divergence():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT value FROM divergence ORDER BY id DESC LIMIT 1')
    divergence = c.fetchone()[0]
    conn.close()
    return round(divergence, 6)  # Округляем значение до 6 знаков после запятой

# Функция для обновления значения дивергенции
def update_divergence(value):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('INSERT INTO divergence (value) VALUES (?)', (value,))
    conn.commit()
    conn.close()
