# Telegram File Converter Bot

Бот для конвертации файлов между различными форматами с интеграцией с Яндекс.Диском для резервного копирования.

# Автор бота 

obbodokk, Обод Даниил

# Имя бота

@F1leConverter_bot

Сыылка на бота: t.me/@F1leConverter_bot

## 🌟 Возможности

- Конвертация между популярными форматами:
  - Документы: DOC, DOCX, PDF, TXT, PPT, XLS и др.
  - Изображения: JPG, PNG, WEBP
  - Аудио: MP3, WAV, FLAC, OGG
  - Видео: MP4, AVI, MKV, WEBM
- Автоматическое определение форматов фото
- Резервное копирование на Яндекс.Диск
- Статистика популярных конвертаций
- Логирование всех операций
- Отправлять погоду по геолокации и назаванию населенного пункта
- Отправлять котиков
- Расшифровывать голосвые сообщения в текст
- Выбирать случайное число или из вариантов

## База данных

- **`data_storage/`** - Директория хранения данных
  - `all_users_logs/` - Логи всех пользователей
  - `geo/` - Геолокационные данные отправленные в бота
  - `logs/` - персональные логи по каждому пользователю (по user_id)
  - `media/` - все загружаемые пользователями файлы
  
## Сторонние бибиотеки для Python 3.13

- `pyTelegramBotAPI`==4.27.0
- `python-dotenv`==1.1.0
- `requests`==2.32.4
- `schedule`==1.2.2
- `vosk`==0.3.45

## Сторонние API

- `Zamzar API` - API для конвертации файлов различных форматов
  - Ссылка: https://developers.zamzar.com/ 
  - В config - ZAMZAR_API_KEY

- `Weather API` - API для получения погоды 
  - Ссылка: https://openweathermap.org/api
  - В config - WEATHER_API_KEY

## Сторонние протоколы

- `YANDEX WEBDAV` - Yandex WebDAV — это способ доступа к Яндекс.Диску как к сетевой папке через стандартный протокол WebDAV (аналог FTP, но поверх HTTP).
  - Ссылка: "https://webdav.yandex.ru" 
  - В config - YANDEX_WEBDAV_URL, YANDEX_LOGIN, YANDEX_WEBDAV_PASSWORD, YANDEX_BACKUP_FOLDER  

## Материалы которыми пользловался

- `ZamzarApi` - https://developers.zamzar.com/docs

- `pyTelegramBotApi` - https://pypi.org/project/pyTelegramBotAPI/, https://pytba.readthedocs.io/ru/latest/

- `Vosk` - https://alphacephei.com/vosk/index.ru

- `Yandex WebDav` - https://yandex.ru/dev/disk/doc/ru/, 

## 🛠 Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/obbodokk/TelegramBotConverter.git
cd TelegramBotConverter