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
    total_counts = sum([count for number, count in Counter(following_numbers).items()])
    predictions = []

    if total_counts > 0:
        counter = Counter(following_numbers)
        num_predictions = 6 if len(following_numbers) >= 6 else 3  # Определяем количество возвращаемых чисел
        most_common = counter.most_common(num_predictions)

        for num, count in most_common:
            probability = round((count / total_counts) * 100, 2)  # Вероятность в процентах
            predictions.append({'number': num, 'probability': f"{probability}%"})
    else:
        predictions.append({"number": "Недостаточно данных", "probability": "0%"})

    return predictions
