document.addEventListener('DOMContentLoaded', function () {
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
            .then(data => {
                predictionElement.innerHTML = ''; // Очистить предыдущие предсказания
                data.predictions.forEach(prediction => {
                    const colorClass = prediction.number === '0' || prediction.number === '00' ? 'green' : (parseInt(prediction.number) % 2 === 0 ? 'black' : 'red');
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
