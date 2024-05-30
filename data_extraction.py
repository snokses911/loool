import pandas as pd
import sqlite3

# Подключение к базе данных
conn = sqlite3.connect('roulette_data.db')

# Загрузка данных из базы данных в DataFrame
query = "SELECT * FROM roulette_numbers"  # Измените запрос в соответствии с вашей структурой таблицы
df = pd.read_sql_query(query, conn)

# Закрытие соединения с базой данных
conn.close()
# Сохранение DataFrame в файл CSV
df.to_csv('data_export.csv', index=False)
# Проверьте первые несколько строк DataFrame, чтобы убедиться, что данные загружены корректно
print(df.head())