import requests
from config import WEATHER_API_KEY

def weather_by_location(lat, lon):
    url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": lat,
        "lon": lon,
        "units": "metric",
        "lang": "ru",
        "appid": WEATHER_API_KEY 
    }
    try:
        response = requests.get(url, params=params)
        data = response.json()

        if response.status_code != 200:
            return "❌ Не удалось получить данные о погоде."

        return (
            f"🌤 Погода в {data.get('name', 'неизвестный город')}:\n\n"
            f"☁️ Описание: {data['weather'][0]['description'].capitalize()}\n"
            f"🌡 Температура: {data['main']['temp']}°C\n"
            f"🧣 Ощущается как: {data['main']['feels_like']}°C\n"
            f"💧 Влажность: {data['main']['humidity']}%\n"
            f"🌬 Скорость ветра: {data['wind']['speed']} м/с"
        )
    except Exception as e:
        return f"⚠ Произошла ошибка: {str(e)}"

def weather_by_name(city):
    geocode_url = "http://api.openweathermap.org/geo/1.0/direct"
    params_geocode = {
        "q": city,
        "limit": 1,
        "appid": WEATHER_API_KEY 
    }
    try:
        geo_r = requests.get(geocode_url, params=params_geocode)
        if geo_r.status_code != 200 or not geo_r.json():
            return f"❌ Город '{city}' не найден."
        data = geo_r.json()[0]
        lat, lon = data["lat"], data["lon"]
        return weather_by_location(lat, lon)
    except Exception as e:
        return f"⚠ Ошибка при поиске города: {str(e)}"