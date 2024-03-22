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
    """Получает числа, следующих за каждым вхождением указанного числа во всей базе данных."""
    conn = connect_db()
    cursor = conn.cursor()
    # Измененный запрос для получения всех следующих чисел после каждого вхождения target_number
    cursor.execute('''
        WITH RankedNumbers AS (
            SELECT number, LEAD(number) OVER (ORDER BY id ASC) AS next_number
            FROM roulette_numbers
        )
        SELECT next_number FROM RankedNumbers
        WHERE number = ? AND next_number IS NOT NULL
    ''', (str(target_number),))
    numbers = cursor.fetchall()
    conn.close()
    # Фильтруем результаты, чтобы исключить возможные None значения
    filtered_numbers = [num[0] for num in numbers if num[0] is not None]

    if not filtered_numbers:
        return [], False  # Возвращает пустой список и False, если данных недостаточно
    return filtered_numbers, True  # Возвращает список следующих чисел и True, если данных достаточно


def delete_last_entry():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, number FROM roulette_numbers ORDER BY id DESC LIMIT 1")
    last_entry = cursor.fetchone()
    if last_entry:
        cursor.execute("DELETE FROM roulette_numbers WHERE id = ?", (last_entry[0],))
        conn.commit()
        deleted_number = last_entry[1]
        conn.close()
        return {"status": "success", "deleted_number": deleted_number}
    else:
        conn.close()
        return {"status": "error", "message": "No entries to delete."}


if __name__ == "__main__":
    create_table()
