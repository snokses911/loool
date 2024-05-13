from flask import Flask, render_template, request, jsonify
import prediction_engine
from data_manager import create_table, insert_number, get_all_numbers, cancel_last_entry
from users_database import register_user, update_user_settings  # Запятая добавлена

app = Flask(__name__)

# Создание таблицы в базе данных при старте приложения
create_table()

@app.route('/')
def index():
    # Здесь будет отображаться интерактивный стол рулетки и предыдущие выборы
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password_hash = request.form.get('password_hash')  # Убедитесь, что пароль хешируется перед сохранением
        profile_picture = request.form.get('profile_picture', 'default.jpg')
        
        # Проверка, что все необходимые поля заполнены
        if username and email and password_hash:
            result = register_user(username, email, password_hash, profile_picture)
            return jsonify(result)
        else:
            return jsonify({'status': 'error', 'message': 'All fields are required.'}), 400
    else:
        # Если метод не POST, то, возможно, вы хотите отобразить страницу с формой регистрации
        return render_template('register.html')

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


@app.route('/cancel_last_entry', methods=['POST'])
def cancel_last_entry():
    # Вызов функции для удаления последней записи из базы данных и получения предыдущего числа
    previous_number, message = cancel_last_entry()
    # Возвращаем предыдущее число и сообщение в формате JSON
    return jsonify({'previous_number': previous_number, 'message': message})



if __name__ == '__main__':
    app.run(debug=True)
