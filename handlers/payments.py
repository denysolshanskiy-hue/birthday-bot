from aiogram import Router, F
from aiogram.types import CallbackQuery

from services.sheets import (
    add_payment,
    payment_exists,
    get_all_users
)

router = Router()


@router.callback_query(F.data.startswith("paid:"))
async def paid_callback(callback: CallbackQuery):
    collection_id = callback.data.split(":")[1]

    user_id = str(callback.from_user.id)

    if not payment_exists(collection_id, user_id):
        await callback.answer(
            "Запис про оплату не знайдено",
            show_alert=True
        )
        return

    # Оновити дату оплати
    add_payment(
        collection_id=collection_id,
        user_id=user_id
    )

    await callback.answer(
        "Оплату зафіксовано ✅",
        show_alert=True
    )
