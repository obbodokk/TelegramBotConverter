from config import CSV_FILE
import csv
import os

# csv сохранение данных юзеров
def csv_create():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['User ID', 'Username', 'First Name'])
            
#проверка на уникальность юзера
def user_check(user_id):
    if not os.path.exists(CSV_FILE):
        return False
    with open(CSV_FILE, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if row and int(row[0]) == user_id:
                return True
    return False

#сохранение пользлователя
def save_csv(user_id, username, first_name):
    if user_check(user_id):
        return
    with open(CSV_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([user_id, username, first_name])