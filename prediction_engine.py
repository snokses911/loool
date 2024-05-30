from collections import Counter
from data_manager import get_following_numbers, get_all_numbers
from datetime import datetime, timedelta

predicted_numbers = []

def predict_next_numbers(current_number):
    following_numbers, data_sufficient = get_following_numbers(current_number)
    all_numbers = get_all_numbers()

    if not data_sufficient:
        return [{"number": "Мало данных для предсказания", "probability": "0%"}]

    total_counts = sum([count for number, count in Counter(following_numbers).items()])
    predictions = []

    if total_counts > 0:
        counter = Counter(following_numbers)
        num_predictions = min(len(following_numbers), 6)
        most_common = counter.most_common(num_predictions)

        # Получаем только наиболее часто встречающиеся числа, которые еще не были предсказаны
        global predicted_numbers
        available_numbers = [num for num, count in most_common if num not in predicted_numbers]
        most_common_predicted = [(num, count) for num, count in most_common if num in available_numbers]

        total_common_counts = sum(count for num, count in most_common_predicted)

        # Определение "New" и "Hot" чисел
        latest_number = all_numbers[-1] if all_numbers else None
        for num, count in most_common_predicted:
            probability = round((count / total_common_counts) * 100, 2)
            prediction = {'number': num, 'probability': f"{probability}%"}
            
            # Пометка "Hot"
            if count / total_common_counts >= 0.5:  # Примерный порог для "Hot" чисел
                prediction['hot'] = True
            
            # Пометка "New"
            if num == latest_number:
                prediction['new'] = True

            predictions.append(prediction)
    else:
        return [{"number": "Мало данных для предсказания", "probability": "0%"}]

    return predictions

def select_number(number):
    global predicted_numbers
    predicted_numbers.append(number)
    return predict_next_numbers(number)