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
                    // Дополнительные заголовки могут потребоваться здесь, если у вас настроена CSRF защита
                },
                // Кодируем выбранное число как часть тела запроса
                body: `number=${encodeURIComponent(selectedNumber)}`
            })
            .then(response => {
                // Проверяем, получен ли корректный ответ
                if (!response.ok) {
                    throw new Error('Network response was not ok ' + response.statusText);
                }
                return response.json();
            }) 
            .then(data => {
                // Обновляем интерфейс с новыми предсказаниями
                const predictionElement = document.getElementById('predictions');
                // Убедитесь, что сервер возвращает свойство 'predictions' в JSON
                predictionElement.textContent = `Следующие числа которые могут выпасть: ${data.predictions.join(', ')}`;
            })
            .catch(error => {
                // Обрабатываем ошибки, если они возникнут
                console.error('Error:', error);
            });
        });
    });
});
