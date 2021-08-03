from bs4 import BeautifulSoup
from datetime import datetime



def get_python_news():
    html = get_html('https://www.python.org/blogs/')
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        all_news = soup.find('ul',
                             class_='list-recent-posts menu').findAll('li')
        result_news = []
        for news in all_news:
            title = news.find('a').text
            url = news.find('a')['href']
            published = news.find('time').text
            try:
                published = datetime.strptime(published, '%B %d, %Y')
            except(ValueError):
                published = datetime.now()
            save_news(title, url, published)


