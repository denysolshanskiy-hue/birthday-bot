from aiogram import Router, F
from aiogram.types import Message

from services.sheets import (
    collections_sheet,
    payments_sheet
)

router = Router()


@router.message(F.text == "🎉 Активні збори")
async def active_collections(
    message: Message
):
    collections = (
        collections_sheet.get_all_records()
    )

    if not collections:
        await message.answer(
            "Активних зборів немає"
        )
        return

    text = "🎉 Активні збори:\n\n"

    for collection in collections[-10:]:
        text += (
            f"#{collection['collection_id']} | "
            f"{collection['birthday_name']} | "
            f"{collection['amount']} грн\n"
        )

    await message.answer(text)


@router.message(F.text == "✅ Оплати")
async def payments_stats(
    message: Message
):
    payments = (
        payments_sheet.get_all_records()
    )

    if not payments:
        await message.answer(
            "Оплат поки немає"
        )
        return

    text = "✅ Останні оплати:\n\n"

    for payment in payments[-10:]:
        text += (
            f"#{payment['collection_id']} | "
            f"{payment['full_name']}\n"
        )

    await message.answer(text)