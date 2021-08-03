import requests
from webapp.db import db
from webapp.news.models import News


def get_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15',
    }
    try:
        result = requests.get(url, headers=headers)
        # print(result.status_code)
        result.raise_for_status()
        return result.text
    except(requests.RequestException, ValueError):
        return False


def save_news(title, url, published):
    news_exists = News.query.filter(News.url == url).count()
    if not news_exists:
        new_news = News(title=title, url=url, published=published)
        db.session.add(new_news)
        db.session.commit()
