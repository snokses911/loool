from collections import Counter
from data_manager import get_following_numbers

# Маппинг чисел рулетки к их цветам, включая "00" как зелёное число
number_to_color = {
    **dict.fromkeys([1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36], "красный"),
    **dict.fromkeys([2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35], "чёрный"),
    **dict.fromkeys([0, "00"], "зелёный")  # Включаем "00"
}

def predict_next_numbers(current_number):
    following_numbers = get_following_numbers(current_number)
    
    if len(following_numbers) < 3:
        return ["Мало данных для предсказания."]
    
    counter = Counter(following_numbers)
    most_common = counter.most_common(3)

    # Добавляем информацию о цвете к прогнозируемым числам
    predictions_with_color = [(str(num), number_to_color.get(str(num), "неизвестно")) for num, _ in most_common]
    
    return predictions_with_color
