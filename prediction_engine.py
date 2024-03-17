from collections import Counter
from data_manager import get_following_numbers

def predict_next_numbers(current_number):
    # Получаем все числа, следующие за указанным
    following_numbers = get_following_numbers(current_number)
    if not following_numbers:
        return []

    # Анализируем, какие числа появляются чаще всего
    counter = Counter(following_numbers)
    most_common = counter.most_common(3)

    # Возвращаем три самых частых числа
    return [number for number, count in most_common]
