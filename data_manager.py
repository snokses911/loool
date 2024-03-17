import sqlite3

DATABASE_NAME = "roulette_data.db"

def connect_db():
    conn = sqlite3.connect(DATABASE_NAME)
    return conn

def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS roulette_numbers (
            id INTEGER PRIMARY KEY,
            number INTEGER NOT NULL
        );
    ''')
    conn.commit()
    conn.close()


def get_all_numbers():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT number FROM roulette_numbers')
    numbers = cursor.fetchall()
    conn.close()
    return [n[0] for n in numbers]

def insert_number(number):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO roulette_numbers (number) VALUES (?)', (number,))
    conn.commit()
    last_id = cursor.lastrowid
    conn.close()
    return last_id

def get_following_numbers(target_number):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT id, number FROM roulette_numbers')
    numbers = cursor.fetchall()
    following_numbers = []
    for i in range(len(numbers) - 1):
        if numbers[i][1] == target_number:
            sequence = [numbers[j][1] for j in range(i + 1, min(i + 4, len(numbers)))]
            following_numbers.extend(sequence)
    conn.close()
    return following_numbers
