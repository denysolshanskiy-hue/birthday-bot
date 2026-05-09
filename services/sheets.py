import gspread
from oauth2client.service_account import ServiceAccountCredentials

from utils.normalize import normalize_name

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    "data/credentials.json",
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
    birthday_name: str,
    birthday_date: str,
    amount: int
):
    collections = collections_sheet.get_all_records()

    collection_id = len(collections) + 1

    collections_sheet.append_row([
        collection_id,
        birthday_name,
        birthday_date,
        amount
    ])

    return collection_id


def add_payment(
    collection_id: int,
    user_id: str,
    full_name: str
):
    payments_sheet.append_row([
        collection_id,
        user_id,
        full_name
    ])


def payment_exists(
    collection_id: int,
    user_id: str
):
    payments = payments_sheet.get_all_records()

    for payment in payments:
        if (
            str(payment["collection_id"]) == str(collection_id)
            and
            str(payment["user_id"]) == str(user_id)
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