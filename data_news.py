import os
import sqlite3

if os.path.exists('hh.sqlite'):
    os.remove('hh.sqlite')

conn = sqlite3.connect('hh.sqlite')
c = conn.cursor()

# Создание таблицы data_news
c.execute('''
    CREATE TABLE IF NOT EXISTS data_news (
        data_date DATE,
        title VARCHAR(255),
        link TEXT
    )
''')

conn.commit()
conn.close()
