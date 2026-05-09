from apscheduler.schedulers.asyncio import AsyncIOScheduler

from services.birthday import (
    get_upcoming_birthdays,
    build_collection_data
)

from services.mailing import send_collection
from datetime import datetime
from services.sheets import get_all_users

async def birthday_check(bot):
    birthdays = get_upcoming_birthdays()

    print(
        f"Знайдено ДН: {len(birthdays)}"
    )

    for birthday_user in birthdays:
        collection = build_collection_data(
            birthday_user
        )

        await send_collection(
            bot,
            collection
        )


def setup_scheduler(bot):
    scheduler = AsyncIOScheduler()

    scheduler.add_job(
        birthday_check,
        trigger="cron",
        hour=10,
        minutes=0
    )
    scheduler.add_job(
        birthday_reminders,
        trigger="cron",
        hour=9,
        minutes=0,
        kwargs={"bot": bot}
    )
    scheduler.start()


async def birthday_reminders(bot):
    today = datetime.now()

    day = today.day
    month = today.month

    users = get_all_users()

    for user in users:
        birthday = user["ДН"]

        try:
            parts = birthday.split(".")

            b_day = int(parts[0])
            b_month = int(parts[1])

        except:
            continue

        if day == b_day and month == b_month:
            await bot.send_message(
                chat_id=444726017,
                text=(
                    f"🎉 Сьогодні день народження у:\n\n"
                    f"{user['ПІБ']}"
                )
            )