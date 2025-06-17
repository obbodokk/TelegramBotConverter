import os
import requests
import time
from config import ZAMZAR_API_KEY, MEDIA_DIR
from utils.logger import log_user_message
from services.convert_stats import log_of_convertation

def convert_handle(bot, message, source_format, target_format):
    chat_id = message.chat.id
    user_id = message.from_user.id
    username = message.from_user.username
    
    temp_path = None
    result_path = None
    
    try:
        file_id, file_name, actual_format = None, None, None

        if source_format == "auto":
            if message.photo:
                file_id = message.photo[-1].file_id
                actual_format = "jpg"  
                file_name = f"photo.{actual_format}"
            elif message.document:
                file_ext = message.document.file_name.split('.')[-1].lower()
                if file_ext in ['jpg', 'jpeg', 'png', 'webp']:
                    file_id = message.document.file_id
                    actual_format = file_ext
                    file_name = message.document.file_name
                else:
                    raise Exception("Пожалуйста, отправьте изображение (JPG/PNG/WEBP)")
            else:
                raise Exception("Пожалуйста, отправьте изображение")
            
            source_format = actual_format
            bot.send_message(chat_id, f"🔍 Определен формат: {source_format.upper()}")
        
        elif source_format in ['doc', 'docx', 'pdf', 'txt', 'ppt', 'pptx', 'xls', 'xlsx', 'csv', 'html']:
            if message.document:
                file_id = message.document.file_id
                file_name = message.document.file_name or f"document.{source_format}"
            else:
                raise Exception("Пожалуйста, отправьте документ")
        
        elif source_format in ['mp4', 'avi', 'mkv', 'webm']:
            if message.video:
                file_id = message.video.file_id
                file_name = f"video.{source_format}"
            elif message.video_note:
                file_id = message.video_note.file_id
                file_name = f"video_note.{source_format}"
            elif message.document:
                file_ext = message.document.file_name.split('.')[-1].lower()
                if file_ext in ['mp4', 'avi', 'mkv', 'webm']:
                    file_id = message.document.file_id
                    file_name = message.document.file_name
                else:
                    raise Exception("Пожалуйста, отправьте видеофайл")
            else:
                raise Exception("Пожалуйста, отправьте видеофайл")
        
        elif source_format in ['mp3', 'wav', 'flac', 'ogg']:
            if message.audio:
                file_id = message.audio.file_id
                file_name = message.document.file_name if message.document else f"audio.{source_format}"
            elif message.voice:
                file_id = message.voice.file_id
                file_name = "voice_message.ogg"
                source_format = "ogg"
            elif message.document:
                file_ext = message.document.file_name.split('.')[-1].lower()
                if file_ext in ['mp3', 'wav', 'flac', 'ogg']:
                    file_id = message.document.file_id
                    file_name = message.document.file_name
                else:
                    raise Exception("Пожалуйста, отправьте аудиофайл")
            else:
                raise Exception("Пожалуйста, отправьте аудиофайл")
        
        if not file_id:
            raise Exception("Не удалось получить файл")

        if file_name and '.' in file_name:
            base_name = file_name.rsplit('.', 1)[0]
            converted_name = f"{base_name}.{target_format}"
        else:
            converted_name = f"converted.{target_format}"

        file_info = bot.get_file(file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        temp_dir = os.path.join(MEDIA_DIR, "temp_conversions")
        os.makedirs(temp_dir, exist_ok=True)
        temp_path = os.path.join(temp_dir, f"temp_{user_id}_{int(time.time())}.{source_format}")
        
        with open(temp_path, 'wb') as f:
            f.write(downloaded_file)

        with open(temp_path, 'rb') as f:
            response = requests.post(
                'https://api.zamzar.com/v1/jobs',
                auth=(ZAMZAR_API_KEY, ''),
                files={'source_file': f},
                data={'target_format': target_format}
            )
            if response.status_code != 201:
                error = response.json().get('errors', [{}])[0].get('message', 'Unknown error')
                raise Exception(f"API Error: {error}")

        job_id = response.json()['id']
        bot.send_message(chat_id, f"🔄 Конвертация начата (ID: {job_id})...")

        result_file_id = None
        for _ in range(30): 
            time.sleep(10)
            job_status = requests.get(
                f'https://api.zamzar.com/v1/jobs/{job_id}',
                auth=(ZAMZAR_API_KEY, '')
            ).json()
            
            if job_status['status'] == 'successful':
                result_file_id = job_status['target_files'][0]['id']
                break
            elif job_status['status'] == 'failed':
                raise Exception("Конвертация не удалась")

        if not result_file_id:
            raise Exception("Превышено время ожидания")


        result_path = os.path.join(temp_dir, converted_name)
        with open(result_path, 'wb') as f:
            f.write(requests.get(
                f'https://api.zamzar.com/v1/files/{result_file_id}/content',
                auth=(ZAMZAR_API_KEY, '')
            ).content)
            
        log_of_convertation(source_format, target_format)#Сбор статистики 

        with open(result_path, 'rb') as f:
            if target_format in ['jpg', 'jpeg']:
                bot.send_photo(chat_id, f, caption=f"✅ {source_format.upper()} → {target_format.upper()}")
            elif target_format == 'png':
                bot.send_document(
                    chat_id, 
                    f,
                    caption=f"✅ {source_format.upper()} → {target_format.upper()}",
                    visible_file_name=converted_name
                )
            elif target_format == 'webp':
                bot.send_document(
                    chat_id,
                    f,
                    caption=f"✅ {source_format.upper()} → {target_format.upper()}",
                    visible_file_name=converted_name
                )
            elif target_format in ['mp4', 'avi', 'mkv', 'webm']:
                bot.send_video(
                    chat_id, 
                    f, 
                    caption=f"✅ {source_format.upper()} → {target_format.upper()}",
                    file_name=converted_name
                )
            elif target_format in ['mp3', 'wav', 'flac', 'ogg']:
                bot.send_audio(
                    chat_id, 
                    f, 
                    caption=f"✅ {source_format.upper()} → {target_format.upper()}",
                    title=converted_name.rsplit('.', 1)[0],
                    performer="Converted file"
                )
            else:
                bot.send_document(
                    chat_id,
                    f,
                    caption=f"✅ {source_format.upper()} → {target_format.upper()}",
                    visible_file_name=converted_name
                )

        log_user_message(user_id, username, f"Конвертация: {source_format}→{target_format}")

    except Exception as e:
        bot.send_message(chat_id, f"❌ Ошибка: {str(e)}")
    finally:
 
        for path in [temp_path, result_path]:
            if path and os.path.exists(path):
                try:
                    os.remove(path)
                except Exception as e:
                    print(f"Ошибка при удалении файла {path}: {e}")
