from collections import Counter
from data_manager import get_following_numbers

predicted_numbers = []

def predict_next_numbers(current_number):
    following_numbers, data_sufficient = get_following_numbers(current_number)

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

        for num, count in most_common_predicted:
            probability = round((count / total_common_counts) * 100, 2)
            predictions.append({'number': num, 'probability': f"{probability}%"})
    else:
        return [{"number": "Мало данных для предсказания", "probability": "0%"}]

    return predictions

def select_number(number):
    global predicted_numbers
    predicted_numbers.append(number)
    return predict_next_numbers(number)
