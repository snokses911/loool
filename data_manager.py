import sqlite3
from datetime import datetime

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
    """
    Вставляет число, текущее время и имя пользователя в базу данных.
    """
    conn = connect_db()
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('INSERT INTO roulette_numbers (number, timestamp, username) VALUES (?, ?, ?)', 
                   (str(number), timestamp, username))  # Преобразование number в строку для поддержки "00"
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
    """
    Получает три числа, следующих за последним вхождением указанного числа.
    """
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT number FROM roulette_numbers WHERE id > (
            SELECT id FROM roulette_numbers WHERE number = ? ORDER BY id DESC LIMIT 1
        ) ORDER BY id ASC LIMIT 3
    ''', (str(target_number),))  # Преобразование target_number в строку для поддержки "00"
    numbers = cursor.fetchall()
    conn.close()
    return [n[0] for n in numbers]

if __name__ == "__main__":
    create_table()
