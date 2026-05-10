from aiogram import Router, F
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery
)

from services.sheets import (
    get_all_users
)

router = Router()


@router.message(F.text == "💳 Картки")
async def cards_menu(
    message: Message
):
    users = get_all_users()

    buttons = []

    for user in users:

        card = str(
            user.get("Card", "")
        ).strip()

        tg_id = str(
            user.get("TG_ID", "")
        ).strip()

        if not card or not tg_id:
            continue

        buttons.append([
            InlineKeyboardButton(
                text=user["ПІБ"],
                callback_data=f"card_{tg_id}"
            )
        ])

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=buttons
    )

    await message.answer(
        "💳 Оберіть людину:",
        reply_markup=keyboard
    )


@router.callback_query(
    F.data.startswith("card_")
)
async def show_card(
    callback: CallbackQuery
):
    tg_id = callback.data.replace(
        "card_",
        ""
    )

    users = get_all_users()

    for user in users:

        if str(user["TG_ID"]) == tg_id:

            card = str(
                user.get("Card", "")
            ).strip()

            if not card:

                await callback.message.answer(
                    "Картка не вказана"
                )

                return

            text = (
                f"💳 {user['ПІБ']}\n\n"
                f"<code>{card}</code>"
            )

            await callback.message.answer(
                text
            )

            return
