import asyncio

from aiogram import Bot
from dotenv import load_dotenv

import os

from services.birthday import (
    get_upcoming_birthdays,
    build_collection_data
)

from services.mailing import send_collection

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)


async def main():
    birthdays = get_upcoming_birthdays(days_ahead=0)

    print("Знайдено ДН:", len(birthdays))

    for birthday_user in birthdays:
        print("Іменинник:", birthday_user["ПІБ"])

        collection = build_collection_data(
            birthday_user
        )

        print(
            "Учасників:",
            len(collection["participants"])
        )

        await send_collection(
            bot,
            collection
        )


asyncio.run(main())