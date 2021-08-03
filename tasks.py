from celery import Celery
from celery.schedules import crontab
from webapp import create_app
from webapp.news.parsers import habr
from webapp.news.telegrambot import bot

flask_app = create_app()
celery_app = Celery('tasks', broker='redis://127.0.0.1:6379/0')


@celery_app.task
def habr_snippets():
    with flask_app.app_context():
        habr.get_news_snippets()


@celery_app.task
def habr_content():
    with flask_app.app_context():
        habr.get_news_content()


@celery_app.task
def send_message():
    with flask_app.app_context():
        bot.send_telegram()


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(minute='*/30'), habr_snippets.s())
    sender.add_periodic_task(crontab(minute='*/30'), habr_content.s())
    sender.add_periodic_task(crontab(minute='*/15'), send_message.s())
