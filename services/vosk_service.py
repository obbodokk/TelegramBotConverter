import os
import wave
import json
import time
import requests
from vosk import Model, KaldiRecognizer
from config import VOSK_MODEL_PATH, MEDIA_DIR, ZAMZAR_API_KEY
from utils.logger import log_user_message
from services.saves_service import save_media_file


try:
    if not os.path.exists(VOSK_MODEL_PATH):
        raise Exception(f"Vosk model не найдена: {VOSK_MODEL_PATH}")
    
    vosk_model = Model(VOSK_MODEL_PATH)
    print("Vosk model загружена")
except Exception as e:
    print(f"Ошибка Vosk model: {e}")
    vosk_model = None

def process_voice_message(bot, message):

    chat_id = message.chat.id
    user_id = message.from_user.id
    username = message.from_user.username or str(user_id)
    
    if not vosk_model:
        bot.send_message(chat_id, "❌ Система распознавания голоса временно недоступна")
        return
    
    try:
        file_id = message.voice.file_id
        original_path = save_media_file(bot, user_id, username, file_id, "voice")
        if not original_path:
            raise Exception("Не удалось сохранить голосовое сообщение")

        bot.send_chat_action(chat_id, 'typing')
        wav_path = convert_ogg_to_wav(bot, message)
        
        if not wav_path:
            raise Exception("Не удалось преобразовать голосовое сообщение в формат WAV.")


        recognized_text = voice_convert_to_text(wav_path)
        
        if not recognized_text:
            raise Exception("Не удалось распознать текст")

     
        response_text = f"🎤 Распознанный текст:\n{recognized_text}"
        bot.send_message(chat_id, response_text)
        log_user_message(user_id, username, f"Распознавание голоса: {recognized_text}")

    except Exception as e:
        error_msg = f"❌ Ошибка: {str(e)}"
        bot.send_message(chat_id, error_msg)
        log_user_message(user_id, username, f"Ошибка распознавания голоса:: {str(e)}")
    
    finally:

        clean_temp_files(user_id)

def convert_ogg_to_wav(bot, message):

    temp_dir = os.path.join(MEDIA_DIR, "temp_voice")
    os.makedirs(temp_dir, exist_ok=True)

    file_info = bot.get_file(message.voice.file_id)
    ogg_data = bot.download_file(file_info.file_path)

    response = requests.post(
        'https://api.zamzar.com/v1/jobs',
        auth=(ZAMZAR_API_KEY, ''),
        files={'source_file': ('voice.ogg', ogg_data)},
        data={'target_format': 'wav'}
    )
    
    if response.status_code != 201:
        raise Exception(f"API error: {response.json().get('errors', [{}])[0].get('message', 'Unknown error')}")

    job_id = response.json()['id']
    

    for _ in range(15):
        time.sleep(2)
        job_status = requests.get(
            f'https://api.zamzar.com/v1/jobs/{job_id}',
            auth=(ZAMZAR_API_KEY, '')
        ).json()
        
        if job_status['status'] == 'successful':
            file_id = job_status['target_files'][0]['id']
            return download_converted_file(file_id, message.from_user.id)
        elif job_status['status'] == 'failed':
            raise Exception("Conversion failed")

    raise Exception("Таймаут преобразования")

def download_converted_file(file_id, user_id):
  
    temp_dir = os.path.join(MEDIA_DIR, "temp_voice")
    wav_path = os.path.join(temp_dir, f"voice_{user_id}_{int(time.time())}.wav")
    
    response = requests.get(
        f'https://api.zamzar.com/v1/files/{file_id}/content',
        auth=(ZAMZAR_API_KEY, ''),
        stream=True
    )
    
    with open(wav_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    
    return wav_path if os.path.exists(wav_path) else None

def voice_convert_to_text(wav_path):

    if not vosk_model or not os.path.exists(wav_path):
        return None
    
    try:
        with wave.open(wav_path, 'rb') as wf:
            if wf.getnchannels() != 1 or wf.getsampwidth() != 2:
                return None
            
            rec = KaldiRecognizer(vosk_model, wf.getframerate())
            rec.SetWords(True)
            
            results = []
            while True:
                data = wf.readframes(4000)
                if len(data) == 0:
                    break
                if rec.AcceptWaveform(data):
                    results.append(json.loads(rec.Result()).get('text', ''))
            
            results.append(json.loads(rec.FinalResult()).get('text', ''))
            return ' '.join(filter(None, results))
    
    except Exception as e:
        print(f"Ошибка распознавания: {e}")
        return None

def clean_temp_files(user_id):

    temp_dir = os.path.join(MEDIA_DIR, "temp_voice")
    if not os.path.exists(temp_dir):
        return
    
    for filename in os.listdir(temp_dir):
        if filename.startswith(f"voice_{user_id}_"):
            try:
                os.remove(os.path.join(temp_dir, filename))
            except:
                pass