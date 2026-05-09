from datetime import datetime, timedelta
import math

from services.sheets import get_all_users

TARGET_AMOUNT = 2000


def parse_birthday(date_str: str):
    try:
        parts = date_str.split(".")

        day = int(parts[0])
        month = int(parts[1])

        return day, month

    except:
        return None


def get_active_users():
    users = get_all_users()

    active_users = []

    for user in users:
        if user["TG_ID"]:
            active_users.append(user)

    return active_users


def get_upcoming_birthdays(days_ahead=2):
    today = datetime.now()
    target_date = today + timedelta(days=days_ahead)

    target_day = target_date.day
    target_month = target_date.month

    upcoming = []

    users = get_all_users()

    for user in users:
        birthday = parse_birthday(user["ДН"])

        if not birthday:
            continue

        day, month = birthday

        if day == target_day and month == target_month:
            upcoming.append(user)

    return upcoming


def calculate_payment_amount(participants_count: int):
    return math.ceil(TARGET_AMOUNT / participants_count)


def build_collection_data(birthday_user):
    active_users = get_active_users()

    participants = []

    for user in active_users:
        if user["TG_ID"] != birthday_user["TG_ID"]:
            participants.append(user)

    amount = calculate_payment_amount(len(participants))

    return {
        "birthday_user": birthday_user,
        "participants": participants,
        "amount": amount
    }