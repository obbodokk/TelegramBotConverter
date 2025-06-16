import requests

def get_address(latitude, longitude):
    url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={latitude}&lon={longitude}"
    headers = {'User-Agent': 'TelegramLocationBot/1.0'}
    
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        
        if 'error' in data:
            return "Не удалось определить адрес для этих координат."
        
        address = data.get('display_name', 'Адрес не найден')
        return address
    except Exception as e:
        print(f"Error getting address: {e}")
        return "Произошла ошибка при определении адреса."