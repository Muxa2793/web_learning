from flask import Flask
from weather import weather_by_city


app = Flask(__name__)


@app.route('/')
def index():
    weather = weather_by_city('Moscow,Russia')
    if weather:
        return f'Температура: {weather["temp"]} градусов, ощущается как: {weather["feels_like"]} градусов.'
    else:
        return 'Сервис погоды временно недоступен'


if __name__ == '__main__':
    app.run(debug=True)
