import time
import os
from schedule import Scheduler
from datetime import datetime
from config import ADMIN_CHAT_ID, ALL_USERS_LOG_DIR
from services.convert_stats import get_top_conversions
from services.yandex_webdav_backup import backup_to_yandex_disk, clean_old_backups

def send_hello(bot):
    greeting_path = "data_storage/hello.txt"
    users_csv = "users.csv"

    try:
        with open(greeting_path, "r", encoding="utf-8") as f:
            greeting_text = f.read()
    except Exception as e:
        print(f"[{datetime.now()}] Не удалось прочитать файл приветствия: {e}")
        return

    try:
        import csv
        with open(users_csv, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                chat_id = row.get("User ID")
                if chat_id:
                    try:
                        bot.send_message(chat_id, greeting_text)
                        print(f"[{datetime.now()}] Приветствие отправлено {chat_id}")
                    except Exception as e:
                        print(f"[{datetime.now()}] Не удалось отправить сообщение {chat_id}: {e}")
                time.sleep(0.3)  # Уменьшил задержку для ускорения
    except Exception as e:
        print(f"[{datetime.now()}] Ошибка при чтении CSV: {e}")

def send_all_logs_to_admin(bot):
    global_log_path = os.path.join(ALL_USERS_LOG_DIR, "all_log.txt")

    if not os.path.exists(global_log_path):
        print(f"[{datetime.now()}] Файл логов не найден: {global_log_path}")
        return

    try:
        with open(global_log_path, "rb") as f:
            bot.send_document(
                ADMIN_CHAT_ID, 
                f, 
                caption="📊 Логи бота за день",
                disable_notification=True
            )
        print(f"[{datetime.now()}] Общий лог отправлен админу")
    except Exception as e:
        print(f"[{datetime.now()}] Ошибка при отправке лога: {e}")
    try:
        with open(global_log_path, "w", encoding="utf-8") as f:
            f.truncate(0)
        print(f"[{datetime.now()}] Общий лог очищен")
    except Exception as e:
        print(f"[{datetime.now()}] Ошибка при очистке лога: {e}")

def send_conversion_stats(bot):
    try:
        top_conversions = get_top_conversions(10)
        
        if not top_conversions:
            bot.send_message(ADMIN_CHAT_ID, "📊 Статистика конвертаций: данных пока нет")
            return
            
        message = "📊 Топ-10 популярных конвертаций:\n\n"
        for i, conv in enumerate(top_conversions, 1):
            message += (
                f"{i}. {conv['source_format'].upper()} → {conv['target_format'].upper()} "
                f"(использовано {conv['count']} раз)\n"
            )
        
        bot.send_message(ADMIN_CHAT_ID, message, disable_notification=True)
        print(f"[{datetime.now()}] Статистика конвертаций отправлена админу")
        
    except Exception as e:
        error_msg = f"Ошибка при формировании статистики: {str(e)}"
        print(f"[{datetime.now()}] {error_msg}")
        bot.send_message(ADMIN_CHAT_ID, f"❌ {error_msg}")

def start_scheduler(bot):
    scheduler = Scheduler()

    #Приветствие
    scheduler.every().day.at("08:00").do(send_hello, bot=bot)
    
    #Логи и статистика админо
    scheduler.every().day.at("23:50").do(send_conversion_stats, bot=bot)
    scheduler.every().day.at("23:55").do(send_all_logs_to_admin, bot=bot)
    
    #Резервное копирование каждые 3 часов
    scheduler.every(3).hours.do(backup_to_yandex_disk)
   
    #Очистка старых бэкапов раз в день
    scheduler.every().day.at("04:00").do(clean_old_backups)

    print(f"[{datetime.now()}] Планировщик запущен")

    try:
        while True:
            scheduler.run_pending()
            time.sleep(1)
    except Exception as e:
        error_msg = f"Критическая ошибка в планировщике: {str(e)}"
        print(f"[{datetime.now()}] {error_msg}")
        bot.send_message(ADMIN_CHAT_ID, f"🔥 {error_msg}")
        raise