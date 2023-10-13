from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import sqlite3


app = Flask(__name__)

def get_news(keyword):
    url = 'https://ria.ru/world/'
    response = requests.get(url)

    news_list = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        titles = soup.find_all(class_='list-item__title')
        dates = soup.find_all(class_='list-item__date')

        for title, date in zip(titles, dates):
            article_title = title.text.strip()
            article_link = title['href']
            publication_time = date.text.strip()

            if keyword in article_title:
                news_list.append({'title': article_title, 'link': article_link, 'time': publication_time})

                # Сохранение данных в SQLite базу данных
                conn = sqlite3.connect('hh.sqlite')
                c = conn.cursor()
                c.execute("INSERT INTO data_news (data_date, title, link) VALUES (?, ?, ?)",
                          (publication_time, article_title, article_link))
                conn.commit()
                conn.close()

    return news_list


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search_results', methods=['POST'])
def search_results():
    keyword = request.form['keyword']
    news_list = get_news(keyword)
    return render_template('search_results.html', keyword=keyword, news_list=news_list)

@app.route('/all_news')
def all_news():
    news_list = get_news("")
    return render_template('all_news.html', news_list=news_list)

if __name__ == '__main__':
    app.run(debug=True)









