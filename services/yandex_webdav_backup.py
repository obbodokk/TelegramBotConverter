import os
import requests
import zipfile
import time
from datetime import datetime
from base64 import b64encode
from config import DATA_DIR,YANDEX_WEBDAV_URL, YANDEX_LOGIN, YANDEX_WEBDAV_PASSWORD, YANDEX_BACKUP_FOLDER

def create_zip_archive():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    zip_name = f"backup_{timestamp}.zip"
    zip_path = os.path.join(DATA_DIR, zip_name)
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(DATA_DIR):
            for file in files:
                if not file.endswith('.zip'):
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, start=DATA_DIR)
                    zipf.write(file_path, arcname)
    
    return zip_path

def webdav_upload(file_path):
    auth = b64encode(f"{YANDEX_LOGIN}:{YANDEX_WEBDAV_PASSWORD}".encode()).decode()
    headers = {
        "Authorization": f"Basic {auth}",
        "Accept": "*/*"
    }
    requests.request(
        "MKCOL", 
        f"{YANDEX_WEBDAV_URL}/{YANDEX_BACKUP_FOLDER}",
        headers=headers
    )
    
    try:
        with open(file_path, 'rb') as f:
            response = requests.put(
                f"{YANDEX_WEBDAV_URL}/{YANDEX_BACKUP_FOLDER}/{os.path.basename(file_path)}",
                data=f,
                headers=headers
            )
        return response.status_code in (200, 201, 204)
    except Exception as e:
        print(f"Ошибка загрузки: {e}")
        return False

def backup_to_yandex_disk():
    try:
        zip_path = create_zip_archive()
        
        if webdav_upload(zip_path):
            print(f"[{datetime.now()}] Бэкап успешно загружен на Яндекс.Диск")
        else:
            print(f"[{datetime.now()}] Ошибка загрузки бэкапа")
        
        os.remove(zip_path)  
        
    except Exception as e:
        print(f"[{datetime.now()}] Ошибка при создании бэкапа: {e}")

def clean_old_backups(days=3):
    now = time.time()
    for file in os.listdir(DATA_DIR):
        if file.startswith('backup_') and file.endswith('.zip'):
            file_path = os.path.join(DATA_DIR, file)
            file_age = now - os.path.getmtime(file_path)
            if file_age > days * 24 * 60 * 60:
                try:
                    os.remove(file_path)
                    print(f"Удален старый бэкап: {file}")
                except Exception as e:
                    print(f"Ошибка при удалении {file}: {e}")