import requests
from flask import current_app


def weather_by_city(city_name):
    weather_url = current_app.config['WEATHER_URL']
    params = {
        'q': city_name,
        'appid': current_app.config['WEATHER_API_KEY'],
        'lang': 'ru',
        'units': 'metric'
    }
    try:
        result = requests.get(weather_url, params=params)
        result.raise_for_status()
        weather = result.json()
        if 'list' in weather:
            if 'main' in weather['list'][0]:
                try:
                    return weather['list'][0]['main']
                except(IndexError, TypeError):
                    return False
    except(requests.RequestException, ValueError):
        print('Сетевая ошибка')
        return False
    return False
