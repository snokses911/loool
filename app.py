from flask import Flask, flash, redirect, render_template, request, jsonify, url_for
import prediction_engine
from data_manager import create_table, insert_number, get_all_numbers, cancel_last_entry
from users_database import register_user, update_user_settings  # type: ignore # Запятая добавлена
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
from werkzeug.security import generate_password_hash, check_password_hash
from telegram_auth import login_telegram

app = Flask(__name__)

# Создание таблицы в базе данных при старте приложения
create_table()

app.add_url_rule('/login', 'login_telegram', login_telegram, methods=['GET'])

@app.route('/')
def index():
    # Здесь будет отображаться авторизация через телеграм/Выбор проекта и выбор сервера
    return render_template('index.html')

@app.route('/predicts')
def predicts():
    return render_template('predicts.html')



@app.route('/settings/<username>', methods=['GET'])
def get_user_settings(username):
    user_settings = get_user_settings(username)
    if user_settings:
        return jsonify({'status': 'success', 'user_settings': user_settings})
    else:
        return jsonify({'status': 'error', 'message': 'User not found.'}), 404

@app.route('/settings/<username>', methods=['POST'])
def update_user(username):
    email = request.form.get('email')
    profile_picture = request.form.get('profile_picture', 'default.jpg')
    update_user_settings(username, email, profile_picture)
    return jsonify({'status': 'success', 'message': 'User settings updated successfully.'})

@app.route('/predict', methods=['POST'])
def predict():
    # Получение числа от пользователя
    number = request.form.get('number')
    # Опционально: получение username, если он передается
    username = request.form.get('username', 'default_user')
    # Проверка, что number действительно получено и является числом
    if number is not None:
        try:
            # Преобразуем number в целое число
            number = int(number)
            # Отправляем число в функцию предсказания
            predictions = prediction_engine.predict_next_numbers(number)
            # Вставляем выбранное число в базу данных с username
            insert_number(number, username)
            # Возвращаем предсказания в формате JSON
            return jsonify(predictions=predictions)
        except ValueError:
            # Если произошла ошибка при преобразовании number в int
            return jsonify({'error': 'Invalid number format'}), 400
    else:
        return jsonify({'error': 'Number is required'}), 400
    
    
@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route('/user_guide')
def user_guide():
    return render_template('user_guide.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')





# Тут надо написать функцию возврата Предпоследнего числа после нажания на кнопку отменить последний ввод



if __name__ == '__main__':
       app.run(host='0.0.0.0', port=8080)
