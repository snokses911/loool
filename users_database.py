import sqlite3
from datetime import datetime

DATABASE_NAME = "users_data.db"

def connect_db():
    """Создаёт соединение с базой данных."""
    conn = sqlite3.connect(DATABASE_NAME)
    return conn

def create_tables():
    """Создаёт таблицы в базе данных, если они ещё не существуют."""
    conn = connect_db()
    cursor = conn.cursor()
    
    # Создание таблицы пользователей
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            profile_picture TEXT DEFAULT 'default.jpg'
        );
    ''')
    
    # Создание таблицы для хранения истории игр
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS games_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            game_data TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        );
    ''')
    
    # Создание таблицы для хранения чисел рулетки
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS roulette_numbers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            number TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            username TEXT,
            FOREIGN KEY (username) REFERENCES users (username)
        );
    ''')
    
    conn.commit()
    conn.close()

create_tables()

def register_user(username, email, password_hash, profile_picture='default.jpg'):
    """Регистрирует нового пользователя."""
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO users (username, email, password_hash, profile_picture) VALUES (?, ?, ?, ?)',
                       (username, email, password_hash, profile_picture))
        conn.commit()
        conn.close()
        return {"status": "success", "message": "User registered successfully."}
    except sqlite3.IntegrityError:
        conn.close()
        return {"status": "error", "message": "Username or email already exists."}


def get_user_settings(username):
    """Получает настройки пользователя по его имени."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT email, profile_picture FROM users WHERE username = ?', (username,))
    user_settings = cursor.fetchone()
    conn.close()
    return user_settings

def update_user_settings(username, email, profile_picture):
    """Обновляет настройки пользователя."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET email = ?, profile_picture = ? WHERE username = ?', (email, profile_picture, username))
    conn.commit()
    conn.close()
