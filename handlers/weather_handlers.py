# from utils.logger import log_user_message
# from services.weather_service import weather_by_location, weather_by_name
# from services.saves_service import save_geo
# import json
# from telebot import types

# def weather_handlers(bot):
#     def weather_menu(chat_id, message_id=None):
#         markup = types.InlineKeyboardMarkup(row_width=2)
#         btn_location = types.InlineKeyboardButton("📍 По геолокации", callback_data="get_location")
#         btn_city = types.InlineKeyboardButton("🌆 Ввести город вручную", callback_data="get_city")
#         btn_cancel = types.InlineKeyboardButton("❌ Отмена", callback_data="cancel_weather")
#         markup.add(btn_location, btn_city)
#         markup.add(btn_cancel)
        
#         if message_id:
#             bot.edit_message_text(
#                 "🌤 Выберите способ получения погоды:",
#                 chat_id,
#                 message_id,
#                 reply_markup=markup
#             )
#         else:
#             bot.send_message(chat_id, "🌤 Выберите способ получения погоды:", reply_markup=markup)

#     @bot.message_handler(commands=['weather'])
#     def send_weather_options(message):
#         weather_menu(message.chat.id)
        
#     @bot.callback_query_handler(func=lambda call: call.data in ((
#         "get_location",
#         "get_city",
#         "cancel_weather",
#         "back_to_options"
#     )))
#     def callback(call):
#         try:
#             chat_id = call.message.chat.id
#             message_id = call.message.message_id
#             data = call.data
            
#             if data == "cancel_weather":
#                 bot.clear_step_handler_by_chat_id(chat_id)
#                 bot.edit_message_text("❌ Получение погоды отменено", chat_id, message_id)
#                 return
                
#             if data == "back_to_options":
#                 weather_menu(chat_id, message_id)
#                 return
                
#             if data == "get_location":
#                 markup = types.InlineKeyboardMarkup()
#                 markup.add(
#                     types.InlineKeyboardButton("◀️ Назад", callback_data="back_to_options"),
#                     types.InlineKeyboardButton("❌ Отмена", callback_data="cancel_weather")
#                 )
#                 sent_msg = bot.edit_message_text(
#                     "📍 Отправьте своё местоположение.",
#                     chat_id,
#                     message_id,
#                     reply_markup=markup
#                 )
#                 bot.register_next_step_handler_by_chat_id(chat_id, w_location, sent_msg.message_id)
                
#             elif data == "get_city":
#                 markup = types.InlineKeyboardMarkup()
#                 markup.add(
#                     types.InlineKeyboardButton("◀️ Назад", callback_data="back_to_options"),
#                     types.InlineKeyboardButton("❌ Отмена", callback_data="cancel_weather")
#                 )
#                 sent_msg = bot.edit_message_text(
#                     "🌆 Введите название города:",
#                     chat_id,
#                     message_id,
#                     reply_markup=markup
#                 )
#                 bot.register_next_step_handler_by_chat_id(chat_id, w_city, sent_msg.message_id)
                
#         except Exception as e:
#             print(f"Ошибка: {e}")

#     def w_location(message, request_message_id):
#         try:
#             bot.delete_message(message.chat.id, request_message_id)
            
#             if message.content_type != 'location':
#                 if message.text and message.text.startswith('/'):
#                     return  
                
#                 markup = types.InlineKeyboardMarkup()
#                 markup.add(
#                     types.InlineKeyboardButton("◀️ Назад", callback_data="back_to_options"),
#                     types.InlineKeyboardButton("❌ Отмена", callback_data="cancel_weather")
#                 )
#                 sent_msg = bot.send_message(message.chat.id, "❌ Ожидалось местоположение. Пожалуйста, отправьте свою геолокацию или нажмите 'Назад'.", reply_markup=markup)
#                 bot.register_next_step_handler_by_chat_id(message.chat.id, w_location, sent_msg.message_id)
#                 return

#             lat = message.location.latitude
#             lon = message.location.longitude
#             user = message.from_user
#             log_user_message(user.id, user.username, "[Геолокация]")
#             save_geo(user.id, user.username, lat, lon)

#             markup = types.InlineKeyboardMarkup()
#             markup.add(
#                 types.InlineKeyboardButton("◀️ Назад", callback_data="back_to_options"),
#                 types.InlineKeyboardButton("❌ Отмена", callback_data="cancel_weather")
#             )
            
#             status_msg = bot.send_message(message.chat.id, "📍 Получаю погоду по вашему местоположению...", reply_markup=markup)
#             weather_info = weather_by_location(lat, lon)
#             bot.delete_message(message.chat.id, status_msg.message_id)
            
#             bot.send_message(message.chat.id, weather_info)
#             weather_menu(message.chat.id)
#         except Exception as e:
#             print(f"Ошибка: {e}")

#     def w_city(message, request_message_id):
#         try:
#             bot.delete_message(message.chat.id, request_message_id)
            
#             if message.text and message.text.startswith('/'):
#                 return
                
#             city = message.text.strip()
#             user = message.from_user
#             user_id = user.id
#             username = user.username
#             log_user_message(user_id, username, f"Ввёл город: {city}")

#             markup = types.InlineKeyboardMarkup()
#             markup.add(
#                 types.InlineKeyboardButton("◀️ Назад", callback_data="back_to_options"),
#                 types.InlineKeyboardButton("❌ Отмена", callback_data="cancel_weather")
#             )
            
#             status_msg = bot.send_message(message.chat.id, f"🌆 Ищу погоду в городе: {city}...", reply_markup=markup)
#             weather_info = weather_by_name(city)
#             bot.delete_message(message.chat.id, status_msg.message_id)
            
#             bot.send_message(message.chat.id, weather_info)
#             weather_menu(message.chat.id)
#         except Exception as e:
#             print(f"Ошибка: {e}")

#     with open('config.json', 'r', encoding='utf-8') as f:
#         config_data = json.load(f)
#     CITIES = config_data.get("CITIES", [])

#     @bot.message_handler(func=lambda message: message.text == "Получить погоду🌤")
#     def send_weather_from_config(message):
#         try:
#             user = message.from_user
#             user_id = user.id
#             username = user.username

#             log_user_message(user_id, username, "Запросил погоду по списку городов")

#             markup = types.InlineKeyboardMarkup()
#             markup.add(
#                 types.InlineKeyboardButton("◀️ Назад", callback_data="back_to_options"),
#                 types.InlineKeyboardButton("❌ Отмена", callback_data="cancel_weather")
#             )
            
#             status_msg = bot.send_message(message.chat.id, "🌤 Получаю данные о погоде...", reply_markup=markup)

#             for city in CITIES:
#                 weather_info = weather_by_name(city)
#                 bot.send_message(message.chat.id, weather_info)

#             bot.delete_message(message.chat.id, status_msg.message_id)
#             bot.send_message(message.chat.id, "✅ Вот погода по выбранным городам:")
#         except Exception as e:
#             print(f"Ошибка: {e}")
from utils.logger import log_user_message
from services.weather_service import weather_by_location, weather_by_name
from services.saves_service import save_geo
import json
from telebot import types

def weather_handlers(bot):
    def weather_menu(chat_id, message_id=None):
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn_location = types.InlineKeyboardButton("📍 По геолокации", callback_data="weather_get_location")
        btn_city = types.InlineKeyboardButton("🌆 Ввести город вручную", callback_data="weather_get_city")
        btn_cancel = types.InlineKeyboardButton("❌ Отмена", callback_data="weather_cancel")
        markup.add(btn_location, btn_city)
        markup.add(btn_cancel)
        
        if message_id:
            bot.edit_message_text(
                "🌤 Выберите способ получения погоды:",
                chat_id,
                message_id,
                reply_markup=markup
            )
        else:
            bot.send_message(chat_id, "🌤 Выберите способ получения погоды:", reply_markup=markup)

    @bot.message_handler(commands=['weather'])
    def send_weather_options(message):
        weather_menu(message.chat.id)
        
    @bot.callback_query_handler(func=lambda call: call.data.startswith('weather_'))
    def weather_callback(call):
        try:
            chat_id = call.message.chat.id
            message_id = call.message.message_id
            data = call.data
            
            if data == "weather_cancel":
                bot.clear_step_handler_by_chat_id(chat_id)
                bot.edit_message_text("❌ Получение погоды отменено", chat_id, message_id)
                return
                
            if data == "weather_back":
                weather_menu(chat_id, message_id)
                return
                
            if data == "weather_get_location":
                markup = types.InlineKeyboardMarkup()
                markup.add(
                    types.InlineKeyboardButton("◀️ Назад", callback_data="weather_back"),
                    types.InlineKeyboardButton("❌ Отмена", callback_data="weather_cancel")
                )
                sent_msg = bot.edit_message_text(
                    "📍 Отправьте своё местоположение.",
                    chat_id,
                    message_id,
                    reply_markup=markup
                )
                bot.register_next_step_handler_by_chat_id(chat_id, w_location, sent_msg.message_id)
                
            elif data == "weather_get_city":
                markup = types.InlineKeyboardMarkup()
                markup.add(
                    types.InlineKeyboardButton("◀️ Назад", callback_data="weather_back"),
                    types.InlineKeyboardButton("❌ Отмена", callback_data="weather_cancel")
                )
                sent_msg = bot.edit_message_text(
                    "🌆 Введите название города:",
                    chat_id,
                    message_id,
                    reply_markup=markup
                )
                bot.register_next_step_handler_by_chat_id(chat_id, w_city, sent_msg.message_id)
                
        except Exception as e:
            print(f"Ошибка: {e}")

    def w_location(message, request_message_id):
        try:
            bot.delete_message(message.chat.id, request_message_id)
            
            if message.content_type != 'location':
                if message.text and message.text.startswith('/'):
                    return  
                
                markup = types.InlineKeyboardMarkup()
                markup.add(
                    types.InlineKeyboardButton("◀️ Назад", callback_data="weather_back"),
                    types.InlineKeyboardButton("❌ Отмена", callback_data="weather_cancel")
                )
                sent_msg = bot.send_message(message.chat.id, "❌ Ожидалось местоположение. Пожалуйста, отправьте свою геолокацию или нажмите 'Назад'.", reply_markup=markup)
                bot.register_next_step_handler_by_chat_id(message.chat.id, w_location, sent_msg.message_id)
                return

            lat = message.location.latitude
            lon = message.location.longitude
            user = message.from_user
            log_user_message(user.id, user.username, "[Геолокация]")
            save_geo(user.id, user.username, lat, lon)

            markup = types.InlineKeyboardMarkup()
            markup.add(
                types.InlineKeyboardButton("◀️ Назад", callback_data="weather_back"),
                types.InlineKeyboardButton("❌ Отмена", callback_data="weather_cancel")
            )
            
            status_msg = bot.send_message(message.chat.id, "📍 Получаю погоду по вашему местоположению...", reply_markup=markup)
            weather_info = weather_by_location(lat, lon)
            bot.delete_message(message.chat.id, status_msg.message_id)
            
            bot.send_message(message.chat.id, weather_info)
            weather_menu(message.chat.id)
        except Exception as e:
            print(f"Ошибка: {e}")

    def w_city(message, request_message_id):
        try:
            bot.delete_message(message.chat.id, request_message_id)
            
            if message.text and message.text.startswith('/'):
                return
                
            city = message.text.strip()
            user = message.from_user
            user_id = user.id
            username = user.username
            log_user_message(user_id, username, f"Ввёл город: {city}")

            markup = types.InlineKeyboardMarkup()
            markup.add(
                types.InlineKeyboardButton("◀️ Назад", callback_data="weather_back"),
                types.InlineKeyboardButton("❌ Отмена", callback_data="weather_cancel")
            )
            
            status_msg = bot.send_message(message.chat.id, f"🌆 Ищу погоду в городе: {city}...", reply_markup=markup)
            weather_info = weather_by_name(city)
            bot.delete_message(message.chat.id, status_msg.message_id)
            
            bot.send_message(message.chat.id, weather_info)
            weather_menu(message.chat.id)
        except Exception as e:
            print(f"Ошибка: {e}")

    @bot.message_handler(func=lambda message: message.text == "Получить погоду🌤")
    def send_weather_from_config(message):
        try:
            user = message.from_user
            user_id = user.id
            username = user.username

            log_user_message(user_id, username, "Запросил погоду по списку городов")

            with open('config.json', 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            CITIES = config_data.get("CITIES", [])

            markup = types.InlineKeyboardMarkup()
            markup.add(
                types.InlineKeyboardButton("◀️ Назад", callback_data="weather_back"),
                types.InlineKeyboardButton("❌ Отмена", callback_data="weather_cancel")
            )
            
            status_msg = bot.send_message(message.chat.id, "🌤 Получаю данные о погоде...", reply_markup=markup)

            for city in CITIES:
                weather_info = weather_by_name(city)
                bot.send_message(message.chat.id, weather_info)

            bot.delete_message(message.chat.id, status_msg.message_id)
            bot.send_message(message.chat.id, "✅ Вот погода по выбранным городам")
        except Exception as e:
            print(f"Ошибка: {e}")