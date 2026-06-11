from aiogram import Router, F
from aiogram.types import Message
from services.sheets import (
    get_last_collection,
    get_collection_payments,
    get_all_users
)
from services.sheets import (
    collections_sheet,
    payments_sheet
)
from datetime import datetime

payments_sheet.append_row([
    collection_id,
    user_id,
    full_name,
    datetime.now().strftime("%d.%m.%Y %H:%M")
])
from services.sheets import (
    get_all_users
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

#============================ Payments ===========================
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
#============================== Statistic =================================
@router.message(F.text == "📊 Статистика")
async def statistics(
    message: Message
):
    users = get_all_users()

    collections = (
        collections_sheet.get_all_records()
    )

    payments = (
        payments_sheet.get_all_records()
    )

    active_users = [
        user for user in users
        if str(user["TG_ID"]).strip()
    ]

    text = (
        "📊 Статистика бота\n\n"

        f"👥 Учасників: {len(users)}\n"
        f"✅ Авторизованих: {len(active_users)}\n"
        f"🎉 Зборів: {len(collections)}\n"
        f"💸 Оплат: {len(payments)}"
    )

    await message.answer(text)

#========================== Users ==================================
@router.message(F.text == "👥 Учасники")
async def participants(
    message: Message
):
    users = get_all_users()

    active_users = [
        user for user in users
        if str(user["TG_ID"]).strip()
    ]

    if not active_users:
        await message.answer(
            "Немає авторизованих учасників"
        )
        return

    text = "👥 Учасники:\n\n"

    for user in active_users:
        text += (
            f"• {user['ПІБ']}\n"
        )

    await message.answer(text)
#========================== not paid ==================================
@router.message(F.text == "❌ Не оплатили")
async def unpaid_users(
    message: Message
):
    collections = (
        collections_sheet.get_all_records()
    )

    payments = (
        payments_sheet.get_all_records()
    )

    if not collections:
        await message.answer(
            "Активних зборів немає"
        )
        return

    latest_collection = collections[-1]

    participants = str(
        latest_collection["participants"]
    ).split(",")

    paid_users = [
        payment["user_id"]
        for payment in payments
        if str(payment["collection_id"])
        ==
        str(latest_collection["collection_id"])
    ]

    unpaid = [
        user_id
        for user_id in participants
        if user_id not in paid_users
    ]

    users = get_all_users()

    unpaid_names = []

    for user in users:
        if str(user["TG_ID"]) in unpaid:
            unpaid_names.append(
                user["ПІБ"]
            )

    if not unpaid_names:
        await message.answer(
            "✅ Усі оплатили"
        )
        return

    text = (
        "❌ Не оплатили:\n\n"
    )

    for name in unpaid_names:
        text += f"• {name}\n"

    await message.answer(text)

@router.message(F.text == "🚀 Тестовий збір")
async def test_collection(message: Message):
    from services.birthday import (
        get_upcoming_birthdays,
        build_collection_data
    )

    from services.mailing import (
        send_collection
    )

    birthdays = get_upcoming_birthdays(2)

    if not birthdays:
        await message.answer(
            "Найближчих ДН не знайдено"
        )
        return

    for birthday_user in birthdays:

        collection = build_collection_data(
            birthday_user
        )

        await send_collection(
            message.bot,
            collection
        )

    await message.answer(
        "✅ Збір запущено"
    )
@router.message(F.text == "❌ Не оплатили")
async def not_paid_handler(message: Message):

    collection = get_last_collection()

    if not collection:
        await message.answer(
            "Активних зборів немає"
        )
        return

    participant_ids = str(
        collection["participants"]
    ).split(",")

    payments = get_collection_payments(
        collection["collection_id"]
    )

    paid_ids = {
        str(payment["user_id"])
        for payment in payments
    }

    users = get_all_users()

    not_paid = []

    for user in users:

        tg_id = str(user["TG_ID"])

        if (
            tg_id
            and
            tg_id in participant_ids
            and
            tg_id not in paid_ids
        ):
            not_paid.append(user["ПІБ"])

    if not not_paid:
        await message.answer(
            "✅ Усі учасники оплатили"
        )
        return

    text = (
        f"❌ Не оплатили ({len(not_paid)}):\n\n"
        + "\n".join(
            f"• {name}"
            for name in not_paid
        )
    )

    await message.answer(text)
