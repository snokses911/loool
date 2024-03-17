document.addEventListener('DOMContentLoaded', function () {
    // Находим все элементы с классом roulette-number
    const rouletteNumbers = document.querySelectorAll('.roulette-number');

    // Добавляем каждому числу обработчик события клика
    rouletteNumbers.forEach(function (numberElement) {
        numberElement.addEventListener('click', function () {
            // Получаем значение data-number, которое соответствует выбранному числу
            const selectedNumber = this.getAttribute('data-number');

            // Отправляем выбранное число на сервер с помощью fetch API
            fetch('/predict', {
                method: 'POST', // Метод HTTP запроса
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                // Кодируем выбранное число как часть тела запроса
                body: `number=${selectedNumber}`
            })
            .then(response => response.json()) // Преобразуем ответ от сервера в JSON
            .then(data => {
                // Обновляем интерфейс с новыми предсказаниями
                const predictionElement = document.querySelector('#predictions');
                predictionElement.innerHTML = `Next numbers might be: ${data.predictions.join(', ')}`;
            })
            .catch(error => console.error('Error:', error));
        });
    });
});
