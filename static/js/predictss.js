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
    const loadingIndicator = document.getElementById('loadingIndicator');
    const errorElement = document.getElementById('error');
    const predictionElement = document.getElementById('predictions');
    const tableButtons = document.querySelectorAll('.table-number');

    rouletteNumbers.forEach(function (numberElement) {
        numberElement.addEventListener('click', function () {
            const selectedNumber = numberElement.getAttribute('data-number');
            loadingIndicator.style.display = 'block';
            errorElement.style.display = 'none';
    
            // Проверяем, выбраны ли имя пользователя и номер стола
            const username = localStorage.getItem('username');
            const tableNumber = localStorage.getItem('tableNumber');
    
            fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `number=${encodeURIComponent(selectedNumber)}&username=${encodeURIComponent(username)}&tableNumber=${encodeURIComponent(tableNumber)}`
            })
            .then(response => {
                loadingIndicator.style.display = 'none';
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                predictionElement.innerHTML = '';
                data.predictions.forEach(prediction => {
                    const colorClass = `${numberToColor[prediction.number]}-background`;
                    const div = document.createElement('div');
                    div.classList.add('prediction-item');
                    div.innerHTML = `
                        <span class="prediction-number ${colorClass}">${prediction.number}</span>
                        <span class="probability">${prediction.probability}</span>
                    `;
                    // Добавляем метки "New" и "Hot" если они присутствуют в данных
                    if (prediction.hot) {
                        const hotLabel = document.createElement('span');
                        hotLabel.classList.add('label', 'hot');
                        hotLabel.textContent = 'Hot';
                        div.appendChild(hotLabel);
                    }
                    if (prediction.new) {
                        const newLabel = document.createElement('span');
                        newLabel.classList.add('label', 'new');
                        newLabel.textContent = 'New';
                        div.appendChild(newLabel);
                    }
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
    
    // Обработчики для выбора номера стола
    tableButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            tableButtons.forEach(function(btn) { btn.classList.remove('selected'); });
            this.classList.add('selected');
            localStorage.setItem('tableNumber', this.dataset.number);
        });
    });
    // Устанавливаем обработчик события клика для кнопки "Отменить последний ввод"
    document.getElementById('cancel-last-entry').addEventListener('click', function() {
        cancelLastEntry(); // Вызов функции при нажатии на кнопку
    });

// Функция вызывается при нажатии на кнопку "Отменить последнее число"
function cancelLastEntry() {
    fetch('/cancel_last_entry', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                // Обновляем текст в элементе, который отображает последнее введенное число
                const selectedNumberElement = document.getElementById('selected-number');
                if (selectedNumberElement) {
                    selectedNumberElement.textContent = data.previous_number;
                    // Также необходимо обновить цвет фона в соответствии с числом
                    selectedNumberElement.className = 'selected-number-circle ' + numberToColor[data.previous_number];
                }
            } else {
                // Обработка ошибки
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
})

document.addEventListener('DOMContentLoaded', function() {
    const numbers = document.querySelectorAll('.roulette-number');
    const selectedNumber = document.getElementById('selected-number');

    numbers.forEach(function(number) {
        number.addEventListener('click', function() {
            const selectedValue = this.getAttribute('data-number');
            selectedNumber.textContent = selectedValue;
            // Определение цвета числа
            const color = numberToColor[selectedValue];
            selectedNumber.style.backgroundColor = color;
            // Снимаем выделение со всех номеров рулетки
            numbers.forEach(function(num) {
                num.classList.remove('selected');
            });
            // Выделяем выбранный номер
            this.classList.add('selected');
        });
    });
});

