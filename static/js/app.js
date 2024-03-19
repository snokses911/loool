document.addEventListener('DOMContentLoaded', function () {
    
    
    const numberToColor = {
        // Красные числа
        "1": "red", "3": "red", "5": "red", "7": "red", "9": "red",
        "12": "red", "14": "red", "16": "red", "18": "red", "19": "red",
        "21": "red", "23": "red", "25": "red", "27": "red", "30": "red",
        "32": "red", "34": "red", "36": "red",
        // Чёрные числа
        "2": "black", "4": "black", "6": "black", "8": "black", "10": "black",
        "11": "black", "13": "black", "15": "black", "17": "black", "20": "black",
        "22": "black", "24": "black", "26": "black", "28": "black", "29": "black",
        "31": "black", "33": "black", "35": "black",
        // Зелёные числа
        "0": "green", "00": "green"
    };

    const rouletteNumbers = document.querySelectorAll('.roulette-number');

    rouletteNumbers.forEach(function (number) {
        number.addEventListener('click', function () {
            const selectedNumber = this.getAttribute('data-number');
            const loadingIndicator = document.getElementById('loadingIndicator');
            const errorElement = document.getElementById('error');
            const predictionElement = document.getElementById('predictions');

            // Показываем индикатор загрузки
            loadingIndicator.style.display = 'block';
            // Скрываем предыдущие ошибки
            errorElement.style.display = 'none';

            fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `number=${encodeURIComponent(selectedNumber)}`
            })
            .then(response => {
                loadingIndicator.style.display = 'none'; // Скрываем индикатор загрузки
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            }) 
            
            // Используйте этот маппинг при формировании предсказаний
            .then(data => {
                predictionElement.innerHTML = ''; // Очистить предыдущие предсказания
                data.predictions.forEach(prediction => {
                    const colorClass = `${numberToColor[prediction.number]}-background`; // Используем маппинг для определения цвета
                    const div = document.createElement('div');
                    div.innerHTML = `<span class="prediction-number ${colorClass}">${prediction.number}</span> с вероятностью <span class="probability">${prediction.probability}</span>`;
                    predictionElement.appendChild(div);
                });
            })
            
            .catch(error => {
                errorElement.style.display = 'block';
                errorElement.textContent = 'Ошибка: Не удалось получить предсказание.';
                console.error('Error:', error);
            });
        });
    });
});

// Функция вызывается при нажатии на кнопку "Отменить последнее число"
function cancelLastEntry() {
    fetch('/cancel_last_entry', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                // Обновляем значение в поле ввода на удаленное число
                document.getElementById('last-number').value = data.deleted_number;
            } else {
                // Здесь можно обработать ошибку, если нужно, например, вывести сообщение в консоль
                console.error(data.message);
            }
        })
        .catch(error => console.error('Error:', error));
}

document.addEventListener('DOMContentLoaded', function() {
    // Устанавливаем обработчик события клика для кнопки "Отменить последний ввод"
    document.getElementById('cancel-last-entry').addEventListener('click', function() {
        cancelLastEntry(); // Вызов функции при нажатии на кнопку
    });
});