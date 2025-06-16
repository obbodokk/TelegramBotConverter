from telebot import types

def get_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_location = types.KeyboardButton("📍 Отправить местоположение", request_location=True)
    btn_weather = types.KeyboardButton("Получить погоду🌤")
    btn_cat = types.KeyboardButton("Кота!")
    btn_help = types.KeyboardButton("Помощь")
    btn_convert = types.KeyboardButton("Конвертировать файл") 
    markup.add(btn_location,btn_weather, btn_cat,btn_help, btn_convert)
    return markup
