import requests
import logging

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Ваш токен бота, который вы получите у BotFather в Telegram
TOKEN = 'my token'

def start(update):
    """Отправляет приветственное сообщение и список команд."""
    message = ("Добро пожаловать в бота RoulePredict для прогнозирования чисел рулетки на GTA5 RP!\n"
               "/go - Запустить приложение\n"
               "/status - Текущий статус и остаток предсказаний\n"
               "/plan - Выбрать тарифный план\n"
               "/info - Информация о программе\n"
               "/help - Помощь и список команд")
    send_message(update['message']['chat']['id'], message)

def go(update):
    """Запускает приложение для прогнозирования."""
    app_name = "Предсказатель Рулетки"  # Название вашего приложения
    game_link = f" https://t.me/rpvrp_bot/rpvrp" # Ссылка на приложениме
    message = f"Приложение '{app_name}' запускается. Ссылка на игру: {game_link}"
    send_message(update['message']['chat']['id'], message)


def status(update):
    """Показывает информацию о тарифе и остатке предсказаний."""
    # Примерный текст, нужна реализация логики
    send_message(update['message']['chat']['id'], "Ваш текущий тарифный план: Базовый. Остаток предсказаний: 10.")

def plan(update):
    """Предоставляет информацию о тарифных планах и позволяет выбрать план."""
    # Примерный текст, нужна реализация логики
    send_message(update['message']['chat']['id'], "Доступные тарифные планы: Базовый, Продвинутый, Премиум. Для выбора напишите /choose_plan [название плана].")

def info(update):
    """Предоставляет информацию о программе и инструкции по использованию."""
    send_message(update['message']['chat']['id'], "RoulePredict помогает прогнозировать исходы в рулетке GTA5 RP, повышая ваши шансы на успех.")

def help_command(update):
    """Отображает список команд и их описание."""
    send_message(update['message']['chat']['id'], "Список команд: /start, /go, /status, /plan, /info, /help.")

def get_updates(offset=None):
    """Получает обновления от Telegram API."""
    url = f'https://api.telegram.org/bot{TOKEN}/getUpdates'
    params = {'offset': offset} if offset else {}
    response = requests.get(url, params=params)
    return response.json()

def send_message(chat_id, text):
    """Отправляет сообщение пользователю."""
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    payload = {'chat_id': chat_id, 'text': text}
    response = requests.post(url, json=payload)
    return response.json()

def main():
    """Главная функция бота."""
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if updates['ok']:
            for update in updates['result']:
                message = update.get('message')
                if message:
                    command = message.get('text')
                    if command == '/start':
                        start(update)
                    elif command == '/go':
                        go(update)
                    elif command == '/status':
                        status(update)
                    elif command == '/plan':
                        plan(update)
                    elif command == '/info':
                        info(update)
                    elif command == '/help':
                        help_command(update)
            # Обновляем last_update_id, чтобы не получать повторные обновления
            results = updates['result']
            if results:
                last_update_id = results[-1]['update_id'] + 1

if __name__ == '__main__':
    main()
