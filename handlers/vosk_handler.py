import threading
from telebot import types
from services.vosk_service import process_voice_message

voice = {}

def voice_handlers(bot):
    @bot.message_handler(commands=['voice'])
    def handle_voice_command(message):
        cleanup_previous_messages(bot, message.chat.id)
        
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("❌ Отменить", callback_data="cancel_voice_record"))
        
        sent = bot.send_message(
            message.chat.id,
            "🎤 Отправьте голосовое сообщение для распознавания текста",
            reply_markup=markup
        )
        
        voice[message.chat.id] = {
            'status': 'waiting',
            'instruction_msg_id': sent.message_id
        }

        threading.Timer(60.0, lambda: auto_delete(bot, message.chat.id, sent.message_id)).start()

    @bot.message_handler(content_types=['voice'])
    def handle_voice(message):
        chat_id = message.chat.id
        
        if chat_id in voice and voice[chat_id]['status'] == 'waiting':
            voice[chat_id].update({
                'status': 'processing'
            })
            
            try:
                bot.delete_message(chat_id, voice[chat_id]['instruction_msg_id'])
            except:
                pass
            
            processing_msg = bot.send_message(chat_id, "🔍 Обрабатываю голосовое сообщение...")
            voice[chat_id]['processing_msg_id'] = processing_msg.message_id
            
            thread = threading.Thread(
                target=process_voice,
                args=(bot, message, chat_id)
            )
            thread.start()

    @bot.callback_query_handler(func=lambda call: call.data == 'cancel_voice_record')
    def handle_cancel_voice(call):
        chat_id = call.message.chat.id
        
        if chat_id in voice:
            bot.answer_callback_query(call.id, "Распознавание отменено")
            clean_messages(bot, chat_id)
            del voice[chat_id]

    def process_voice(bot, message, chat_id):
        try:
            result = process_voice_message(bot, message)
            
            if chat_id in voice and 'processing_msg_id' in voice[chat_id]:
                try:
                    bot.delete_message(chat_id, voice[chat_id]['processing_msg_id'])
                except:
                    pass
            
            if result:
                bot.send_message(chat_id, f"🎤 Результат распознавания:\n{result}")
            
        except:
            bot.send_message(chat_id, "❌ Произошла ошибка при обработке голосового сообщения")
        finally:
            if chat_id in voice:
                del voice[chat_id]

    def auto_delete(bot, chat_id, msg_id):
        if chat_id in voice and voice[chat_id]['status'] == 'waiting':
            try:
                bot.delete_message(chat_id, msg_id)
                del voice[chat_id]
            except:
                pass

    def clean_messages(bot, chat_id):
        if chat_id not in voice:
            return
            
        v = voice[chat_id]
        try:
            if 'instruction_msg_id' in v:
                bot.delete_message(chat_id, v['instruction_msg_id'])
            if 'processing_msg_id' in v:
                bot.delete_message(chat_id, v['processing_msg_id'])
        except:
            pass

    def cleanup_previous_messages(bot, chat_id):
        if chat_id in voice:
            clean_messages(bot, chat_id)
            del voice[chat_id]