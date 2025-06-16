import os
from datetime import datetime
from utils.logger import lock
from config import MEDIA_DIR, GEO_DIR

# Сохранение медиафайлов
def save_media_file(bot, user_id, username, file_id, file_type):
    try:
        file_info = bot.get_file(file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        user_media_dir = os.path.join(MEDIA_DIR, f"{user_id}_{username}")
        os.makedirs(user_media_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        ext = file_info.file_path.split('.')[-1]
        filename = f"{file_type}_{timestamp}.{ext}"
        file_path = os.path.join(user_media_dir, filename)

        with open(file_path, 'wb') as new_file:
            new_file.write(downloaded_file)

        return file_path
    except Exception as e:
        print("Ошибка при сохранении медиа:", e)
        return None

# Сохранение геолокации
def save_geo(user_id, username, latitude, longitude):
    if username:
        filename = f"{user_id}_{username}.txt"
    else:
        filename = f"{user_id}.txt"

    geo_path = os.path.join(GEO_DIR, filename)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        with lock:
            with open(geo_path, "a", encoding="utf-8") as f:
                f.write(f"[{timestamp}] Получены координаты: {latitude}, {longitude}\n")
        print(f"Координаты записаны в {geo_path}")
    except Exception as e:
        print(f"Не удалось записать геолокацию: {e}")
