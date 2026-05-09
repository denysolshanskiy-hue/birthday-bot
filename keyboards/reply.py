from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton
)


admin_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(
                text="📊 Статистика"
            )
        ],
        [
            KeyboardButton(
                text="🎉 Активні збори"
            )
        ],
        [
            KeyboardButton(
                text="✅ Оплати"
            )
        ],
        [
            KeyboardButton(
                text="👥 Учасники"
            )
        ]
    ],
    resize_keyboard=True
)