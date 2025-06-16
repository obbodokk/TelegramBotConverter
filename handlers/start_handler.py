
from database.user_db import user_check, save_csv
from utils.logger import log_user_message
from utils.keyboard_utils import get_keyboard

def start_handlers(bot):
    @bot.message_handler(commands=['start'])
    def start(message):
        user = message.from_user
        user_id = user.id
        username = user.username
        first_name = user.first_name

        log_user_message(user_id, username, "/start")

        if user_check(user_id):
            bot.send_message(message.chat.id, "*Рад снова видеть тебя\\❗️Какую задачу выполнить❓*", parse_mode='MarkdownV2')
        else:
            bot.send_message(message.chat.id, f"Привет, {first_name or 'пользователь'}!")

        save_csv(user_id, username, first_name)
        bot.send_message(message.chat.id, "_Выберите опцию:_",parse_mode='MarkdownV2', reply_markup=get_keyboard()) 