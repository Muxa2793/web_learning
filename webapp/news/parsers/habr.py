from bs4 import BeautifulSoup
from datetime import datetime
from webapp.news.parsers.utils import get_html, save_news
from webapp.news.models import News
from webapp.db import db


def get_news_snippets():
    html = get_html('https://habr.com/ru/rss/search/?q=python++++++++&order_by=date++++++++&target_type=posts++++++++&hl=ru++++++++&fl=ru&fl=ru')
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        
        title_list = []
        url_news_list = []
        pub_date_list = []

        title_news = soup.find_all('title')
        for title in title_news[2:]:
            title_list.append(title.text)
        # print(title_list)
        
        url_news = soup.find_all('guid', text=True)
        for url in url_news:
            url_news_list.append(url.text)
        # print(url_news_list)
        
        pub_date_news = soup.find_all('pubdate')
        for pub_date in pub_date_news[1:]:
            pub_date_list.append(pub_date.text)
        # print(pub_date_list)

        for title, url, published in zip(title_list, url_news_list, pub_date_list):
            try:
                published = datetime.strptime(published, '%a, %d %b %Y %X GMT')
            except(ValueError):
                published = datetime.now()
            save_news(title, url, published)


def get_news_content():
    news_without_text = News.query.filter(News.text.is_(None))
    for news in news_without_text:
        html = get_html(news.url)
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            news_text = soup.find('div', class_='tm-article-body').decode_contents()
            if news_text:
                news.text = news_text
                db.session.add(news)
                db.session.commit()
