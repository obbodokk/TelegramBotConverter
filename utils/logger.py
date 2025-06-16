import os
from datetime import datetime
import threading
from config import LOGS_DIR, ALL_USERS_LOG_DIR
lock = threading.Lock()

# Логирование текстовых сообщений каждого пользователя отдельно
def log_user_message(user_id, username, message_text):
    if username:
        filename = f"{user_id}_{username}.txt"
    else:
        filename = f"{user_id}.txt"

    user_log_path = os.path.join(LOGS_DIR, filename)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    all_user_log_path = os.path.join(ALL_USERS_LOG_DIR,"all_log.txt")
    with lock:
        with open(user_log_path, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {message_text}\n")
    with lock:
            with open(all_user_log_path, "a", encoding="utf-8") as f_global:
                f_global.write(f"[{timestamp}] [{user_id}] {message_text}\n")   # Запись в общий файл

