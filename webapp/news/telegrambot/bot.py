import requests
import re
from webapp.news.models import News
from webapp import db
from webapp.settings import BOT_TOKEN, CHANEL_ID


def send_telegram():
    """Функция для отправки сообщений в телеграм-канал, которые содержат ссылки на новости"""

    token = BOT_TOKEN
    url = "https://api.telegram.org/bot"
    channel_id = CHANEL_ID
    url += token
    method = url + "/sendMessage"

    # Ищем новости, которые ещё не были отправлены
    not_sended_news = News.query.filter(News.sended.is_(None))

    # Если такие новости найдены, то отправляем
    # ссылку на новость с помощью API телеграма
    if not_sended_news:
        for news in not_sended_news:
            # Создаём текст сообщения
            text = create_text(news.url)
            # Отправляем сообщение в телеграм-канал
            r = requests.post(method, data={"chat_id": channel_id, "text": text})
            if r.status_code != 200:
                raise Exception("post_text error")
            if r.status_code == 200:
                news.sended = 'SENDED'
                db.session.add(news)
                db.session.commit()
            break
    else:
        pass


def create_text(url):
    """Функция для генерации текста сообщения в зависимости от источника"""

    # Используем регулярные выражения
    # для выявления совпадений по начальным
    # буквам url, которые известны нам заранее
    if re.match(r'https://habr.com', url):
        text = f'Новости Python\n#habr #PythonHub\n{url}'

    # Если совпадение не найдено,
    # то используем стандартное сообщение
    else:
        text = f'#PythonNews\n{url}'
    return text
