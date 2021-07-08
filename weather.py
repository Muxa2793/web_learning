import requests
from settings import API_KEY


def weather_by_city(city_name):
    weather_url = 'http://api.openweathermap.org/data/2.5/find'
    params = {
        'q': city_name,
        'appid': API_KEY,
        'lang': 'ru',
        'units': 'metric'
    }
    result = requests.get(weather_url, params=params)
    weather = result.json()
    if 'list' in weather:
        if 'main' in weather['list'][0]:
            try:
                return weather['list'][0]['main']
            except(IndexError, TypeError):
                return False
    return False


# if __name__ == '__main__':
#     weather_by_city('Moscow,Russia')
