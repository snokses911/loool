import sqlite3
from datetime import datetime
from collections import Counter

DATABASE_NAME = "roulette_data.db"

def connect_db():
    """Создаёт соединение с базой данных."""
    conn = sqlite3.connect(DATABASE_NAME)
    return conn

def create_table():
    """Создаёт таблицу в базе данных, если она ещё не существует."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS roulette_numbers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            number TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            username TEXT NOT NULL
        );
    ''')
    conn.commit()
    conn.close()

def insert_number(number, username):
    """Вставляет число, текущее время и имя пользователя в базу данных."""
    conn = connect_db()
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('INSERT INTO roulette_numbers (number, timestamp, username) VALUES (?, ?, ?)',
                   (str(number), timestamp, username))
    conn.commit()
    conn.close()

def get_all_numbers():
    """Возвращает список всех чисел из таблицы roulette_numbers."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT number FROM roulette_numbers')
    numbers = cursor.fetchall()
    conn.close()
    return [n[0] for n in numbers]

def get_following_numbers(target_number):
    """Получает числа, следующих за каждым вхождением указанного числа."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM roulette_numbers WHERE number = ?', (str(target_number),))
    ids = [id_[0] for id_ in cursor.fetchall()]

    following_numbers = []
    for id_ in ids:
        cursor.execute('SELECT number FROM roulette_numbers WHERE id > ? ORDER BY id ASC LIMIT 1', (id_,))
        next_number = cursor.fetchone()
        if next_number:
            following_numbers.append(next_number[0])

    conn.close()
    if not following_numbers:
        return [], False  # Возвращает пустой список и False, если данных недостаточно
    return following_numbers, True  # Возвращает список следующих чисел и True, если данных достаточно

if __name__ == "__main__":
    create_table()
