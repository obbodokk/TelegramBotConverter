import telebot
import os
import threading
from config import TOKEN, LOGS_DIR, MEDIA_DIR, GEO_DIR, ALL_USERS_LOG_DIR
from database.user_db import csv_create
from handlers.start_handler import start_handlers
from handlers.other_command_handler import other_command_handler
from handlers.weather_handlers import weather_handlers
from handlers.saves_handlers import saves_handlers
from handlers.cat_handler import cat_handler
from handlers.convert_handler import convert_handler
from handlers.vosk_handler import voice_handlers
from services.scheduler import start_scheduler


bot = telebot.TeleBot(TOKEN)

os.makedirs(LOGS_DIR, exist_ok=True)
os.makedirs(MEDIA_DIR, exist_ok=True)
os.makedirs(GEO_DIR, exist_ok=True)
os.makedirs(ALL_USERS_LOG_DIR, exist_ok=True)

csv_create()

start_handlers(bot)
convert_handler(bot) 
weather_handlers(bot)
voice_handlers(bot)
cat_handler(bot)  
other_command_handler(bot)
saves_handlers(bot)  

threading.Thread(target=start_scheduler, args=(bot,), daemon=True).start()
print('Бот запущен')
bot.infinity_polling()

