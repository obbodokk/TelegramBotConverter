from telebot import types
from services.convert_service import handle_conversion
import time

user_states = {}

def convert_handler(bot):
    @bot.message_handler(func=lambda message: message.text == "Конвертировать файл")
    def ask_file_type(message):
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("📄 Документ", callback_data="convert_document"),
            types.InlineKeyboardButton("🖼️ Фото", callback_data="convert_photo_auto"),
            types.InlineKeyboardButton("🎥 Видео", callback_data="convert_video"),
            types.InlineKeyboardButton("🔊 Аудио", callback_data="convert_audio"),
            types.InlineKeyboardButton("❌ Отмена", callback_data="cancel_conversion")
        )
        user_states[message.chat.id] = {
            "stage": "file_type_selection",
            "messages_to_delete": []
        }
        sent = bot.send_message(message.chat.id, "📁 Выберите тип файла для конвертации:", reply_markup=markup)
        user_states[message.chat.id]["messages_to_delete"].append(sent.message_id)

    @bot.callback_query_handler(func=lambda call: call.data.startswith((
        "convert_", "doc_", "photo_", "video_", "audio_", "conv_",
        "cancel_conversion", "back"
    )))
    def handle_callback(call):
        chat_id = call.message.chat.id
        data = call.data
        
        if data == "cancel_conversion":
            cleanup_conversion_state(bot, chat_id)
            bot.answer_callback_query(call.id, "Конвертация отменена")
            return
            
        if data == "back":
            handle_back(bot, call)
            return
            
        if data.startswith("convert_"):
            if data == "convert_photo_auto":
                handle_photo_auto_selection(bot, call)
            else:
                handle_file_type_selection(bot, call)
        elif data.startswith(("doc_", "photo_", "video_", "audio_")):
            handle_source_format_selection(bot, call)
        elif data.startswith("conv_"):
            handle_conversion_selection(bot, call)

    def handle_photo_auto_selection(bot, call):
        chat_id = call.message.chat.id
        
        user_states[chat_id] = {
            "stage": "target_format_selection",
            "file_type": "photo",
            "source_format": "auto",
            "messages_to_delete": user_states.get(chat_id, {}).get("messages_to_delete", [])
        }
        
        show_photo_target_formats(bot, chat_id)

    def show_photo_target_formats(bot, chat_id):
        target_formats = [
            ("PNG", "conv_photo_auto_png"),
            ("JPG", "conv_photo_auto_jpg"),
            ("WEBP", "conv_photo_auto_webp"),
            ("PDF", "conv_photo_auto_pdf")
        ]
        
        markup = types.InlineKeyboardMarkup(row_width=2)
        for i in range(0, len(target_formats), 2):
            row = target_formats[i:i+2]
            markup.add(*[types.InlineKeyboardButton(text, callback_data=cb) for text, cb in row])
        
        markup.add(
            types.InlineKeyboardButton("◀️ Назад", callback_data="back"),
            types.InlineKeyboardButton("❌ Отмена", callback_data="cancel_conversion")
        )
        
        safe_delete_messages(bot, chat_id)
        sent = bot.send_message(
            chat_id,
            "🖼️ Выберите в какой формат конвертировать фото:",
            reply_markup=markup
        )
        user_states[chat_id]["messages_to_delete"].append(sent.message_id)

    def handle_back(bot, call):
        chat_id = call.message.chat.id
        state = user_states.get(chat_id, {})
        
        safe_delete_messages(bot, chat_id)
        
        if state.get("stage") == "target_format_selection":
            if state.get("source_format") == "auto":
                ask_file_type_via_callback(bot, chat_id)
            else:
                show_source_formats(bot, chat_id, state["file_type"])
            state["stage"] = "source_format_selection"
        elif state.get("stage") == "source_format_selection":
            ask_file_type_via_callback(bot, chat_id)
            state["stage"] = "file_type_selection"

    def ask_file_type_via_callback(bot, chat_id):
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("📄 Документ", callback_data="convert_document"),
            types.InlineKeyboardButton("🖼️ Фото", callback_data="convert_photo_auto"),
            types.InlineKeyboardButton("🎥 Видео", callback_data="convert_video"),
            types.InlineKeyboardButton("🔊 Аудио", callback_data="convert_audio"),
            types.InlineKeyboardButton("❌ Отмена", callback_data="cancel_conversion")
        )
        
        sent = bot.send_message(
            chat_id,
            "📁 Выберите тип файла для конвертации:",
            reply_markup=markup
        )
        user_states[chat_id]["messages_to_delete"].append(sent.message_id)

    def handle_file_type_selection(bot, call):
        chat_id = call.message.chat.id
        file_type = call.data.split("_")[1]
        
        user_states[chat_id] = {
            "stage": "source_format_selection",
            "file_type": file_type,
            "messages_to_delete": user_states.get(chat_id, {}).get("messages_to_delete", [])
        }
        
        show_source_formats(bot, chat_id, file_type)

    def show_source_formats(bot, chat_id, file_type):
        formats = {
            "document": [
                ("DOC", "doc_doc"), ("DOCX", "doc_docx"), 
                ("PDF", "doc_pdf"), ("TXT", "doc_txt"),
                ("PPT", "doc_ppt"), ("PPTX", "doc_pptx"),
                ("XLS", "doc_xls"), ("XLSX", "doc_xlsx"), 
                ("CSV", "doc_csv"), ("HTML", "doc_html")
            ],
            "photo": [
                ("JPG", "photo_jpg"), ("PNG", "photo_png"),
                ("WEBP", "photo_webp")
            ],
            "video": [
                ("MP4/Кружки", "video_mp4"), ("AVI", "video_avi"),
                ("MKV", "video_mkv"), ("WEBM", "video_webm")
            ],
            "audio": [
                ("MP3", "audio_mp3"), ("WAV", "audio_wav"),
                ("FLAC", "audio_flac"), ("OGG/Голосовые сообщения", "audio_ogg")
            ]
        }.get(file_type, [])

        markup = types.InlineKeyboardMarkup(row_width=2)
        for i in range(0, len(formats), 2):
            row = formats[i:i+2]
            markup.add(*[types.InlineKeyboardButton(text, callback_data=cb) for text, cb in row])
        
        markup.add(
            types.InlineKeyboardButton("◀️ Назад", callback_data="back"),
            types.InlineKeyboardButton("❌ Отмена", callback_data="cancel_conversion")
        )
        
        safe_delete_messages(bot, chat_id)
        sent = bot.send_message(
            chat_id,
            f"Выберите исходный формат:",
            reply_markup=markup
        )
        user_states[chat_id]["messages_to_delete"].append(sent.message_id)

    def handle_source_format_selection(bot, call):
        chat_id = call.message.chat.id
        parts = call.data.split("_")
        file_type = parts[0]
        source_format = parts[1]
        
        user_states[chat_id].update({
            "stage": "target_format_selection",
            "source_format": source_format,
            "messages_to_delete": user_states.get(chat_id, {}).get("messages_to_delete", [])
        })
        
        show_target_formats(bot, chat_id, file_type, source_format)

    def show_target_formats(bot, chat_id, file_type, source_format):
        conversions = {
            "doc_doc": ["docx", "pdf", "html", "txt", "png", "jpg"],
            "doc_docx": ["doc", "pdf", "html", "txt", "png", "jpg"],
            "doc_pdf": ["doc", "docx", "png", "jpg", "ppt", "pptx", "xls", "xlsx"],
            "doc_txt": ["doc", "docx", "pdf", "html", "png", "jpg"],
            "doc_ppt": ["pdf", "png", "jpg", "html"],
            "doc_pptx": ["pdf", "png", "jpg", "html"],
            "doc_xls": ["xlsx", "csv", "pdf", "txt", "html", "png", "jpg"],
            "doc_xlsx": ["xls", "csv", "pdf", "txt", "html", "png", "jpg"],
            "doc_csv": ["xlsx", "xls", "doc", "html", "pdf"],
            "doc_html": ["doc", "docx", "pdf", "txt"],
            "photo_jpg": ["png", "pdf", "webp"],
            "photo_png": ["jpg", "pdf", "webp"],
            "photo_webp": ["png", "jpg"],
            "video_mp4": ["mp3", "wav", "avi", "mkv", "webm"],
            "video_avi": ["mp3", "wav", "mp4", "mkv", "webm"],
            "video_mkv": ["mp3", "wav", "mp4", "avi", "webm"],
            "video_webm": ["mp3", "wav", "mp4", "avi", "mkv"],
            "audio_mp3": ["wav", "flac", "ogg"],
            "audio_wav": ["mp3", "flac", "ogg"],
            "audio_flac": ["mp3", "wav", "ogg"],
            "audio_ogg": ["mp3", "wav", "flac"]
        }.get(f"{file_type}_{source_format}", [])

        markup = types.InlineKeyboardMarkup(row_width=2)
        for target in conversions:
            btn_text = f"{source_format.upper()} → {target.upper()}"
            if file_type == "video" and target in ["mp3", "wav"]:
                btn_text += " 🔊"
            markup.add(types.InlineKeyboardButton(
                btn_text, 
                callback_data=f"conv_{file_type}_{source_format}_{target}"
            ))
        
        markup.add(
            types.InlineKeyboardButton("◀️ Назад", callback_data="back"),
            types.InlineKeyboardButton("❌ Отмена", callback_data="cancel_conversion")
        )
        
        safe_delete_messages(bot, chat_id)
        sent = bot.send_message(
            chat_id,
            f"Доступные конвертации для {source_format.upper()}:",
            reply_markup=markup
        )
        user_states[chat_id]["messages_to_delete"].append(sent.message_id)

    def handle_conversion_selection(bot, call):
        chat_id = call.message.chat.id
        parts = call.data.split("_")
        file_type = parts[1]
        source_format = parts[2] if parts[2] != "auto" else "auto"
        target_format = parts[3]
        
        msg = ""
        if source_format == "auto":
            msg = "🖼️ Автоопределение формата фото\n"
            msg += f"Конвертация в: {target_format.upper()}\n"
            msg += "Отправьте фото или изображение"
        elif file_type == "video" and target_format in ["mp3", "wav"]:
            msg = "🎥→🔊 Конвертация видео в аудио\n"
            msg += f"{source_format.upper()} → {target_format.upper()}\n"
            msg += "Отправьте видеофайл"
        elif file_type == "video":
            msg = "🎥 Конвертация видео\n"
            msg += f"{source_format.upper()} → {target_format.upper()}\n"
            msg += "Отправьте видеофайл"
        elif file_type == "audio":
            msg = "🔊 Конвертация аудио\n"
            msg += f"{source_format.upper()} → {target_format.upper()}\n"
            msg += "Отправьте аудиофайл"
        else:
            msg = f"Конвертация: {source_format.upper()} → {target_format.upper()}\n"
            msg += "Отправьте файл для конвертации"
        
        markup = types.InlineKeyboardMarkup()
        markup.row(
            types.InlineKeyboardButton("◀️ Назад", callback_data="back"),
            types.InlineKeyboardButton("❌ Отмена", callback_data="cancel_conversion")
        )
        
        user_states[chat_id].update({
            "source_format": source_format,
            "target_format": target_format,
            "messages_to_delete": user_states.get(chat_id, {}).get("messages_to_delete", [])
        })

        safe_delete_messages(bot, chat_id)
        sent = bot.send_message(chat_id, msg, reply_markup=markup)
        user_states[chat_id]["messages_to_delete"].append(sent.message_id)
        
        bot.register_next_step_handler_by_chat_id(
            chat_id,
            lambda m: handle_file_for_conversion(bot, m, source_format, target_format)
        )

    def handle_file_for_conversion(bot, message, source_format, target_format):
        chat_id = message.chat.id
    
        safe_delete_messages(bot, chat_id)
        
        handle_conversion(bot, message, source_format, target_format)
        
        try:
            bot.delete_message(chat_id, message.message_id)
        except Exception as e:
            print(f"Ошибка при удалении сообщения с файлом: {e}")

    def safe_delete_messages(bot, chat_id):

        if chat_id not in user_states or "messages_to_delete" not in user_states[chat_id]:
            return
            
        for msg_id in user_states[chat_id]["messages_to_delete"]:
            try:
                bot.delete_message(chat_id, msg_id)
                time.sleep(0.1) 
            except Exception as e:

                if "message to delete not found" not in str(e):
                    print(f"Ошибка при удалении сообщения {msg_id}: {e}")
    
        user_states[chat_id]["messages_to_delete"] = []

    def cleanup_conversion_state(bot, chat_id):
        safe_delete_messages(bot, chat_id)
        if chat_id in user_states:
            del user_states[chat_id]