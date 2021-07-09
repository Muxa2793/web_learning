from flask import Flask, render_template
from weather import weather_by_city


app = Flask(__name__)


@app.route('/')
def index():
    weather = weather_by_city('Moscow,Russia')
    page_title = 'Прогноз погоды'
    return render_template('index.html',
                           page=page_title,
                           weather=weather)


if __name__ == '__main__':
    app.run(debug=True)
