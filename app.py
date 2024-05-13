from flask import Flask, render_template, request, jsonify
import prediction_engine
from data_manager import create_table, insert_number, get_all_numbers, delete_last_entry  # Запятая добавлена

app = Flask(__name__)

# Создание таблицы в базе данных при старте приложения
create_table()

@app.route('/')
def index():
    # Здесь будет отображаться интерактивный стол рулетки и предыдущие выборы
    return render_template('index.html')

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

@app.route('/cancel_last_entry', methods=['POST'])
def cancel_last_entry():
    # Вызов функции для удаления последней записи из базы данных и получения предыдущего числа
    previous_number, message = delete_last_entry()
    # Возвращаем предыдущее число и сообщение в формате JSON
    return jsonify({'previous_number': previous_number, 'message': message})

if __name__ == '__main__':
    app.run(debug=True)
