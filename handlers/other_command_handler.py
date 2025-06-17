import json
from utils.logger import log_user_message
from services.roll_service import process_roll
from services.send_all_logs import send_all_logs_to_admin
from services.get_adress_service import get_address
from services.convert_stats import get_top_conversions
from config import ADMIN_CHAT_ID

def other_command_handler(bot):
    @bot.message_handler(func=lambda message: message.text == "Помощь")
    def button_help(message):
        if message.from_user.id == ADMIN_CHAT_ID:#Отдельное меню для админа
            help_text = '''📋 *Основные команды* 📋
\\/start — Начало работы с ботом
\\/about — Информация об авторе
\\/help — Это меню

🌦 *Погода*:
\\/weather — Узнать погоду по геолокации или названию города

🎤 *Голос*:
\\/voice — Распознавание голосовых сообщений

🎲 *Случайный выбор*:
\\/roll — Случайное число или выбор из вариантов
*Примеры:*
_\\/roll — Случайное число_  
_\\/roll 10 — Число от 1 до 10_  
_\\/roll 56 78 — Выберет один из вариантов_
_\\/roll Яблоко Банан — Выберет один из вариантов_

🫅*Только для админа*:
\\/logs — Отправить логи сообщений всех пользователей в чат
\\/stats — Статистика популярных форматов

📊*Статистика*:
Бот автоматически отправляет:
08:00 — Утреннее приветствие
23:55 — Статистика конвертаций и логи бота
'''
        else:
            #Для обычных пользователей
            help_text = '''📋 *Основные команды* 📋
\\/start — Начало работы с ботом
\\/about — Информация об авторе
\\/help — Это меню

🌦 *Погода*:
\\/weather — Узнать погоду по геолокации или названию города

🎤 *Голос*:
\\/voice — Распознавание голосовых сообщений

🎲 *Случайный выбор*:
\\/roll — Случайное число или выбор из вариантов
*Примеры:*
_\\/roll — Случайное число_  
_\\/roll 10 — Число от 1 до 10_  
_\\/roll 56 78 — Выберет один из вариантов_
_\\/roll Яблоко Банан — Выберет один из вариантов_
'''
        bot.send_message(message.chat.id, help_text, parse_mode='MarkdownV2')
        
    @bot.message_handler(commands=['help'])
    def help(message):
        if message.from_user.id == ADMIN_CHAT_ID:#Отдельное меню для админа
            help_text = '''📋 *Основные команды* 📋
\\/start — Начало работы с ботом
\\/about — Информация об авторе
\\/help — Это меню

🌦 *Погода*:
\\/weather — Узнать погоду по геолокации или названию города

🎤 *Голос*:
\\/voice — Распознавание голосовых сообщений

🎲 *Случайный выбор*:
\\/roll — Случайное число или выбор из вариантов
*Примеры:*
_\\/roll — Случайное число_  
_\\/roll 10 — Число от 1 до 10_  
_\\/roll 56 78 — Выберет один из вариантов_
_\\/roll Яблоко Банан — Выберет один из вариантов_

🫅*Только для админа*:
\\/logs — Отправить логи сообщений всех пользователей в чат
\\/stats — Статистика популярных форматов

📊*Статистика*:
Бот автоматически отправляет:
08:00 — Утреннее приветствие
23:55 — Статистика конвертаций и логи бота
'''
        else:
            #Для обычных пользователей
            help_text = '''📋 *Основные команды* 📋
\\/start — Начало работы с ботом
\\/about — Информация об авторе
\\/help — Это меню

🌦 *Погода*:
\\/weather — Узнать погоду по геолокации или названию города

🎤 *Голос*:
\\/voice — Распознавание голосовых сообщений

🎲 *Случайный выбор*:
\\/roll — Случайное число или выбор из вариантов
*Примеры:*
_\\/roll — Случайное число_  
_\\/roll 10 — Число от 1 до 10_  
_\\/roll 56 78 — Выберет один из вариантов_
_\\/roll Яблоко Банан — Выберет один из вариантов_
'''
        bot.send_message(message.chat.id, help_text, parse_mode='MarkdownV2')
            
    @bot.message_handler(commands=['about'])
    def about(message):
        with open('about.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        author_info = f"Автор бота: {data['author']}"
        bot.send_message(message.chat.id, author_info)

    @bot.message_handler(commands=['roll'])
    def roll_command(message):
        user = message.from_user
        user_id = user.id
        username = user.username
        log_user_message(user_id, username, "/roll")

        args = message.text.split()[1:]  
        response = process_roll(args)   
        bot.reply_to(message, response)

    @bot.message_handler(commands=['logs'])
    def handle_logs_command(message):
        if message.chat.id != ADMIN_CHAT_ID and message.from_user.id != ADMIN_CHAT_ID:
            bot.reply_to(message, "⛔ Эта команда доступна только администратору")
            return
        user = message.from_user
        log_user_message(user.id, user.username, "/logs")

        try:
            send_all_logs_to_admin(bot, message.chat.id)
            bot.reply_to(message, "✅ Логи успешно отправлены")
        except Exception as e:
            bot.reply_to(message, f"❌ Ошибка при отправке логов: {e}")
            
    @bot.message_handler(content_types=['location'])
    def handle_location(message):
        if message.location:
            lat = message.location.latitude
            lon = message.location.longitude

            processing_msg = bot.send_message(message.chat.id, "Обрабатываю геолокацию...")
    
            address = get_address(lat, lon)
            
            bot.delete_message(message.chat.id, processing_msg.message_id)
            
            bot.send_message(message.chat.id, f"Адрес этой локации:\n\n{address}")
            
            bot.send_message(message.chat.id, f"Координаты:\nШирота: {lat}\nДолгота: {lon}")
        else:
            bot.send_message(message.chat.id, "Пожалуйста, отправьте геолокацию.")

    @bot.message_handler(commands=['stats'])
    def handle_stats_command(message):
        if message.chat.id != ADMIN_CHAT_ID and message.from_user.id != ADMIN_CHAT_ID:
            bot.reply_to(message, "⛔ Эта команда доступна только администратору")
            return
        
        try:
            top_conversions = get_top_conversions(10)
            
            if not top_conversions:
                bot.reply_to(message, "📊 Статистика конвертаций: данных пока нет")
                return
            
            response = "📊 Топ популярных конвертаций:\n\n"
            for i, conv in enumerate(top_conversions, 1):
                response += (
                    f"{i}. {conv['source_format'].upper()} → {conv['target_format'].upper()} "
                    f"(использовано {conv['count']} раз)\n"
                )
            
            bot.reply_to(message, response)
        except Exception as e:
            bot.reply_to(message, f"❌ Ошибка при получении статистики: {str(e)}")
