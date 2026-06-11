import gspread
from oauth2client.service_account import ServiceAccountCredentials

from utils.normalize import normalize_name

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

import json
import os
from datetime import datetime

credentials_dict = json.loads(
    os.getenv("GOOGLE_CREDENTIALS")
)

credentials = ServiceAccountCredentials.from_json_keyfile_dict(
    credentials_dict,
    scope
)

client = gspread.authorize(credentials)

SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1_WrUdtJB_77hPATyqF6WgaoLJPYfx8n69Ivq7g8zIVA/edit?gid=0#gid=0"

spreadsheet = client.open_by_url(SPREADSHEET_URL)

users_sheet = spreadsheet.worksheet("Users")
collections_sheet = spreadsheet.worksheet("Collections")
payments_sheet = spreadsheet.worksheet("Payments")


def get_all_users():
    users = users_sheet.get_all_records()

    filtered_users = []

    for user in users:
        if user["ПІБ"]:
            filtered_users.append(user)

    return filtered_users


def find_user_by_name(name: str):
    users = get_all_users()

    normalized_input = normalize_name(name)

    for index, user in enumerate(users, start=2):
        normalized_sheet_name = normalize_name(user["ПІБ"])

        if normalized_input == normalized_sheet_name:
            return {
                "row": index,
                "user": user
            }

    return None


def save_telegram_data(row: int, tg_id: int, username: str):
    users_sheet.update_cell(row, 4, str(tg_id))
    users_sheet.update_cell(row, 3, username)


def create_collection(
    birthday_name,
    birthday_date,
    amount,
    participants
):
    collections = collections_sheet.get_all_records()

    collection_id = len(collections) + 1

    collections_sheet.append_row([
    collection_id,
    birthday_name,
    birthday_date,
    amount,
    ",".join([str(p) for p in participants])
])

    return collection_id


def add_all_participants_to_payments(collection_id, birthday_name):
    """Додати всіх авторизованих учасників (окрім іменинника) у payments з порожнім paid_at"""
    users = get_all_users()
    
    for user in users:
        tg_id = str(user["TG_ID"]).strip()
        
        # Пропускаємо іменинника та тих, хто не авторизований
        if not tg_id or user["ПІБ"] == birthday_name:
            continue
        
        payments_sheet.append_row([
            collection_id,
            tg_id,
            user["ПІБ"],
            ""  # paid_at - порожнє
        ])


def add_payment(
    collection_id: int,
    user_id: str
):
    """Оновити дату оплати для існуючого запису у payments"""
    payments = payments_sheet.get_all_records()
    
    for index, payment in enumerate(payments, start=2):
        if (str(payment["collection_id"]) == str(collection_id) and
            str(payment["user_id"]).strip() == str(user_id).strip()):
            # Оновити дату оплати
            payments_sheet.update_cell(
                index, 
                4,  # Колонка paid_at
                datetime.now().strftime("%d.%m.%Y %H:%M")
            )
            return
    
    print(f"Запис не знайдено: collection_id={collection_id}, user_id={user_id}")


def payment_exists(
    collection_id: int,
    user_id: str
):
    payments = payments_sheet.get_all_records()

    for payment in payments:
        if (
            str(payment["collection_id"]) == str(collection_id)
            and
            str(payment["user_id"]).strip() == str(user_id).strip()
        ):
            return True

    return False

def collection_exists(
    birthday_name: str,
    birthday_date: str
):
    collections = collections_sheet.get_all_records()

    for collection in collections:
        if (
            collection["birthday_name"] == birthday_name
            and
            collection["birthday_date"] == birthday_date
        ):
            return True

    return False

def user_already_registered(tg_id: int):
    users = get_all_users()

    for user in users:
        if str(user["TG_ID"]) == str(tg_id):
            return True

    return False
def get_last_collection():
    collections = collections_sheet.get_all_records()

    if not collections:
        return None

    return collections[-1]


def get_collection_payments(collection_id):
    payments = payments_sheet.get_all_records()

    result = []

    for payment in payments:
        if str(payment["collection_id"]) == str(collection_id):
            result.append(payment)

    return result
