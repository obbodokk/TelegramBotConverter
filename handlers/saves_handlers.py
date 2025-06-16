from utils.logger import log_user_message
from services.saves_service import save_media_file
def saves_handlers(bot):
    @bot.message_handler(content_types=['text'])
    def handle_text(message):
        user = message.from_user
        user_id = user.id
        username = user.username
        text = message.text.strip()
        log_user_message(user_id, username, text)

    @bot.message_handler(content_types=['photo'])
    def handle_photo(message):
        user = message.from_user
        user_id = user.id
        username = user.username
        file_id = message.photo[-1].file_id
        log_user_message(user_id, username, "[Фото]")
        save_media_file(bot, user_id, username, file_id, "photo")

    @bot.message_handler(content_types=['video'])
    def handle_video(message):
        user = message.from_user
        user_id = user.id
        username = user.username
        file_id = message.video.file_id
        log_user_message(user_id, username, "[Видео]")
        save_media_file(bot, user_id, username, file_id, "video")

    @bot.message_handler(content_types=['audio'])
    def handle_audio(message):
        user = message.from_user
        user_id = user.id
        username = user.username
        file_id = message.audio.file_id
        log_user_message(user_id, username, "[Аудио]")
        save_media_file(bot, user_id, username, file_id, "audio")

    @bot.message_handler(content_types=['document'])
    def handle_document(message):
        user = message.from_user
        user_id = user.id
        username = user.username
        file_id = message.document.file_id
        log_user_message(user_id, username, "[Документ]")
        save_media_file(bot, user_id, username, file_id, "document")

    @bot.message_handler(content_types=['voice'])
    def handle_voice(message):
        user = message.from_user
        user_id = user.id
        username = user.username
        file_id = message.voice.file_id
        log_user_message(user_id, username, "[Голосовое сообщение]")
        save_media_file(bot, user_id, username, file_id, "voice")

    @bot.message_handler(content_types=['video_note'])
    def handle_video_note(message):
        user = message.from_user
        user_id = user.id
        username = user.username
        file_id = message.video_note.file_id
        log_user_message(user_id, username, "[Кружок]")
        save_media_file(bot, user_id, username, file_id, "video_note")
    
    @bot.message_handler(content_types=['animation'])
    def handle_gif(message):
        user = message.from_user
        user_id = user.id
        username = user.username
        file_id = message.animation.file_id  
        log_user_message(user_id, username, "[GIF]")
        save_media_file(bot, user_id, username, file_id, "gif")