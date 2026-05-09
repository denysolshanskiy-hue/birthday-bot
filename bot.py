from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from handlers.payments import router as payments_router
from dotenv import load_dotenv
from scheduler import setup_scheduler
import asyncio
import os
from handlers.admin import (
    router as admin_router
)
from handlers.start import router as start_router
from handlers.auth import router as auth_router

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

dp = Dispatcher()

dp.include_router(start_router)
dp.include_router(auth_router)
dp.include_router(payments_router)
dp.include_router(admin_router)
async def main():
    print("Bot started")
    setup_scheduler(bot)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())