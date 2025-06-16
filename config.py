from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("TOKEN")
#Апишки
WEATHER_API_KEY = os.getenv("API_WEATHER")
ZAMZAR_API_KEY = os.getenv("API_ZAMZAR")

CSV_FILE = "users.csv"

ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID"))

#Директории
DATA_DIR = 'data_storage'
LOGS_DIR = os.path.join(DATA_DIR, 'logs')
MEDIA_DIR = os.path.join(DATA_DIR, 'media')
GEO_DIR = os.path.join(DATA_DIR, 'geo')
ALL_USERS_LOG_DIR = os.path.join(DATA_DIR, "all_users_logs", "all_users.txt")

VOSK_MODEL_PATH = 'vosk-model-small-ru-0.22'

STATS_FILE = os.path.join(DATA_DIR, 'convert_stats.csv')

#Облачные бекапы
YANDEX_LOGIN = os.getenv("YANDEX_LOGIN")
YANDEX_WEBDAV_PASSWORD = os.getenv("WEB_DAV")  
YANDEX_BACKUP_FOLDER = "tg_bot_backups" 
YANDEX_WEBDAV_URL = "https://webdav.yandex.ru" 