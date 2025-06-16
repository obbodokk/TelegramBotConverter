import requests
from utils.logger import log_user_message

def cat_handler(bot):
    @bot.message_handler(func=lambda message: message.text == "Кота!")
    def catass(message):
        log_user_message(message.from_user.id, message.from_user.username, "Запросил кота")
        cat_url = 'https://cataas.com/cat'
        response = requests.get(cat_url)
        if response.status_code == 200:
            bot.send_photo(message.chat.id, response.content)
        else:
            bot.reply_to(message, "Произошла ошибка при получении изображения кота")