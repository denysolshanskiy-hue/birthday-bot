from aiogram import Router, F
from aiogram.types import Message
from aiogram.types import Message, CallbackQuery
from services.sheets import (
    get_last_collection,
    get_collection_payments,
    get_all_users
)
from services.sheets import (
    collections_sheet,
    payments_sheet
)
from services.sheets import (
    get_all_users
)
router = Router()


@router.message(F.text == "🎉 Активні збори")
async def active_collections(
    message: Message
):
    collections = collections_sheet.get_all_records()

    if not collections:
        await message.answer(
            "Активних зборів немає"
        )
        return

    latest_collection = collections[-1]

    birthday_name = latest_collection["birthday_name"]

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
async def unpaid_users(message: Message):

    payments = payments_sheet.get_all_records()
    users = get_all_users()

    latest_collection = collections_sheet.get_all_records()[-1]

    birthday_name = latest_collection["birthday_name"]

    participant_ids = [
        x.strip()
        for x in str(
            latest_collection["created_at"]
        ).split(",")
    ]

    paid_ids = {
        str(payment["user_id"]).strip()
        for payment in payments
        if str(payment["collection_id"])
        ==
        str(latest_collection["collection_id"])
    }

    unpaid_names = []

    for user in users:

        tg_id = str(
            user["TG_ID"]
        ).strip()

        if not tg_id:
            continue

        if (
            tg_id in participant_ids
            and tg_id not in paid_ids
            and user["ПІБ"] != birthday_name
        ):
            unpaid_names.append(
                user["ПІБ"]
            )

    if not unpaid_names:
        await message.answer(
            "✅ Усі оплатили"
        )
        return

    text = (
        f"❌ Не оплатили ({len(unpaid_names)}):\n\n"
        + "\n".join(
            f"• {name}"
            for name in unpaid_names
        )
    )

    from keyboards.inline import remind_button

    await message.answer(
        text,
        reply_markup=remind_button()
    )
    
@router.callback_query(
    F.data == "remind_unpaid"
)
async def remind_unpaid(
    callback: CallbackQuery
):

    payments = payments_sheet.get_all_records()
    users = get_all_users()

    paid_ids = {
        str(payment["user_id"]).strip()
        for payment in payments
        if str(payment["collection_id"]) == "1"
    }

    reminder_text = (
        "🔔 Нагадування\n\n"
        "Ви ще не підтвердили оплату збору.\n\n"
        "Сума: 143 грн\n\n"
        "https://send.monobank.ua/jar/6siNn8uvXQ"
    )

    count = 0

    for user in users:

        tg_id = str(user["TG_ID"]).strip()

        if (
            tg_id
            and tg_id not in paid_ids
            and user["ПІБ"] != "Бондар Альона Олександрівна"
        ):
            try:

                await callback.bot.send_message(
                    int(tg_id),
                    reminder_text
                )

                count += 1

            except Exception as e:
                print(e)

    await callback.message.edit_reply_markup(
        reply_markup=None
    )

    await callback.message.answer(
        f"🔔 Надіслано нагадування: {count}"
    )

    await callback.answer()
