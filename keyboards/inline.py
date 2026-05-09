from aiogram.utils.keyboard import InlineKeyboardBuilder


def paid_button(collection_id: int):
    builder = InlineKeyboardBuilder()

    builder.button(
        text="✅ Я оплатив",
        callback_data=f"paid:{collection_id}"
    )

    return builder.as_markup()