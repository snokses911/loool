from flask import Flask, request, redirect, url_for, session
import hashlib
import hmac
import json
from urllib.parse import unquote
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app = Flask(__name__)
app.secret_key = b'секретный ключь'  # секретный ключ

# токен бота, полученный от BotFather
BOT_TOKEN = 'токен'

@app.route('/login', methods=['GET'])
def login_telegram():
    # Получаем параметры запроса, отправленные Telegram
    auth_data = request.args.to_dict()

    # Проверяем подпись
    check_hash = auth_data.pop('hash')
    sorted_params = sorted(auth_data.items(), key=lambda x: x[0])
    data_check_string = '\n'.join(['{}={}'.format(k, v) for k, v in sorted_params])
    secret_key = hashlib.sha256(BOT_TOKEN.encode('utf-8')).digest()
    hmac_string = hmac.new(secret_key, data_check_string.encode('utf-8'), hashlib.sha256).hexdigest()

    if hmac_string == check_hash:
        # Подпись верна, пользователь авторизован
        # Здесь вы можете создать сессию пользователя или выполнить другие действия
        session['user_data'] = auth_data
        return redirect(url_for('index'))
    else:
        # Подпись неверна, возможно, это попытка взлома
        return 'Unauthorized', 401

@app.route('/')
def index():
    # Здесь ваш код для отображения главной страницы
    user_data = session.get('user_data', {})
    return f'Привет, {user_data.get("first_name", "Гость")}!'

if __name__ == '__main__':
    app.run(debug=True)