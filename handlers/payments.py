from aiogram import Router, F
from aiogram.types import CallbackQuery

from services.sheets import (
    add_payment,
    payment_exists,
    get_all_users
)
from datetime import datetime

def add_payment(
    collection_id: int,
    user_id: str,
    full_name: str
):
    payments_sheet.append_row([
        collection_id,
        user_id,
        full_name,
        datetime.now().strftime("%d.%m.%Y %H:%M")
    ])
router = Router()


@router.callback_query(F.data.startswith("paid:"))
async def paid_callback(callback: CallbackQuery):
    collection_id = callback.data.split(":")[1]

    user_id = str(callback.from_user.id)

    if payment_exists(collection_id, user_id):
        await callback.answer(
            "Ви вже підтвердили оплату",
            show_alert=True
        )
        return

    full_name = None

    users = get_all_users()

    for user in users:
        if str(user["TG_ID"]) == user_id:
            full_name = user["ПІБ"]
            break

    if not full_name:
        await callback.answer(
            "Користувача не знайдено",
            show_alert=True
        )
        return

    add_payment(
        collection_id=collection_id,
        user_id=user_id,
        full_name=full_name
    )

    await callback.answer(
        "Оплату зафіксовано ✅",
        show_alert=True
    )
