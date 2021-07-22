from flask import Flask, render_template
from webapp.weather import weather_by_city
from webapp.model import db, News
from webapp.forms import LoginForm


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('settings.py')
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URL_EXTERNAL']
    db.init_app(app)

    @app.route('/')
    def index():
        page_title = 'Новости Python'
        weather = weather_by_city(app.config['WEATHER_DEFAULT_CITY'])
        news_list = News.query.order_by(News.published.desc()).all()
        return render_template('index.html',
                               page=page_title,
                               weather=weather,
                               news_list=news_list)

    @app.route('/login')
    def login():
        page_title = 'Авторизация'
        login_form = LoginForm()
        return render_template('login.html',
                               page=page_title,
                               form=login_form)

    return app
