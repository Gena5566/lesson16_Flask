import sqlite3
from prettytable import PrettyTable

# Подключение к базе данных
conn = sqlite3.connect('hh.sqlite')

# Создаем курсор
cursor = conn.cursor()

cursor.execute('SELECT * from data_news')

result = cursor.fetchall()

# Создаем объект таблицы
table = PrettyTable()
table.field_names = ["Дата/Время", "Заголовок", "Ссылка"]

# Добавляем данные из результата запроса в таблицу
for row in result:
    table.add_row(row)

# Выводим таблицу
print(table)

# Закрываем соединение
conn.close()
