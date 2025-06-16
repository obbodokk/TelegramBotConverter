import os
from datetime import datetime
from config import ALL_USERS_LOG_DIR, ADMIN_CHAT_ID

def send_all_logs_to_admin(bot, chat_id=None):
    admin_chat_id = chat_id if chat_id else ADMIN_CHAT_ID
    global_log_path = os.path.join(ALL_USERS_LOG_DIR, "all_log.txt")

    if not os.path.exists(global_log_path):
        error_msg = f"Файл логов не найден: {global_log_path}"
        print(f"[{datetime.now()}] {error_msg}")
        raise FileNotFoundError(error_msg)

    try:
        with open(global_log_path, "rb") as f:
            bot.send_document(admin_chat_id, f, caption="📄 Логи бота")
        print(f"[{datetime.now()}] Логи отправлены в чат {admin_chat_id}")
    except Exception as e:
        error_msg = f"Ошибка при отправке логов: {e}"
        print(f"[{datetime.now()}] {error_msg}")
        raise