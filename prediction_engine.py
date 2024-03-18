from collections import Counter
from data_manager import get_following_numbers

def predict_next_numbers(current_number):
    following_numbers, data_sufficient = get_following_numbers(current_number)

    if not data_sufficient:
        return [{"number": "Мало данных для предсказания", "probability": "0%"}]

    total_counts = sum([count for number, count in Counter(following_numbers).items()])
    predictions = []

    if total_counts > 0:
        counter = Counter(following_numbers)
        # Возвращаем до 6 чисел, если данных достаточно, иначе столько, сколько есть
        num_predictions = min(len(following_numbers), 6)
        most_common = counter.most_common(num_predictions)

        for num, count in most_common:
            probability = round((count / total_counts) * 100, 2)  # Вероятность в процентах
            predictions.append({'number': num, 'probability': f"{probability}%"})
    else:
        return [{"number": "Мало данных для предсказания", "probability": "0%"}]

    return predictions
