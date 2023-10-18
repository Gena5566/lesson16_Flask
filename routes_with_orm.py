from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import requests
from bs4 import BeautifulSoup


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///news.db'  # Путь к базе данных SQLite
db = SQLAlchemy(app)

class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data_date = db.Column(db.String(20))
    title = db.Column(db.String(255))
    link = db.Column(db.String(255))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/news_table')
def news_table():
    news = News.query.all()
    return render_template('news_table.html', news=news)

@app.route('/all_news')
def all_news():
    keyword = ""
    news_list = get_news(keyword)
    return render_template('all_news.html', news_list=news_list)

@app.route('/search_results', methods=['POST'])
def search_results():
    keyword = request.form['keyword']
    news_list = get_news(keyword)
    return render_template('search_results.html', keyword=keyword, news_list=news_list)

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

                if keyword == "":
                    news_entry = News(data_date=publication_time, title=article_title, link=article_link)
                    with app.app_context():
                        db.session.add(news_entry)
                        db.session.commit()

    return news_list

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Создать таблицы в базе данных
    app.run(debug=True)










