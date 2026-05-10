from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton
)


admin_keyboard = ReplyKeyboardMarkup(
            keyboard=[
        [KeyboardButton(text="📊 Статистика"), KeyboardButton(text="🎉 Активні збори")],
        [KeyboardButton(text="✅ Оплати", KeyboardButton(text="👥 Учасники")],
        [KeyboardButton(text="👥 Учасники")]
        [KeyboardButton(text="❌ Не оплатили"), KeyboardButton(text="💳 Картки")],
            ],
                resize_keyboard=True
            )
