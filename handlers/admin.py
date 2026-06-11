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

    collections = collections_sheet.get_all_records()

    if not collections:
        await message.answer(
            "Активних зборів немає"
        )
        return

    latest_collection = collections[-1]

    birthday_name = latest_collection["birthday_name"]
    collection_id = latest_collection["collection_id"]

    payments = payments_sheet.get_all_records()

    # Знайти записи для цього збору без заповненої дати оплати
    unpaid_records = [
        payment for payment in payments
        if (str(payment["collection_id"]) == str(collection_id) and
            not str(payment.get("paid_at", "")).strip())
    ]

    if not unpaid_records:
        await message.answer(
            "✅ Усі оплатили"
        )
        return

    unpaid_names = [
        record["full_name"] 
        for record in unpaid_records
    ]

    text = (
        f"❌ Не оплатили ({len(unpaid_names)}):\n\n"
        +
        "\n".join(
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

    collections = collections_sheet.get_all_records()

    if not collections:
        await callback.answer()
        return

    latest_collection = collections[-1]

    birthday_name = latest_collection["birthday_name"]
    collection_id = latest_collection["collection_id"]

    payments = payments_sheet.get_all_records()

    # Знайти записи для цього збору без заповненої дати оплати
    unpaid_records = [
        payment for payment in payments
        if (str(payment["collection_id"]) == str(collection_id) and
            not str(payment.get("paid_at", "")).strip())
    ]

    reminder_text = (
        "🔔 Нагадування\n\n"
        f"Ви ще не підтвердили оплату збору для "
        f"{birthday_name}.\n\n"
        f"Сума: {latest_collection['amount']} грн\n\n"
        "https://send.monobank.ua/jar/6siNn8uvXQ"
    )

    count = 0
    users = get_all_users()
    user_tg_map = {str(user["TG_ID"]).strip(): user for user in users}

    for record in unpaid_records:
        tg_id = str(record["user_id"]).strip()
        
        try:
            await callback.bot.send_message(
                int(tg_id),
                reminder_text
            )
            count += 1

        except Exception as e:
            print(f"Помилка надсилання {record['full_name']}: {e}")

    await callback.message.edit_reply_markup(
        reply_markup=None
    )

    await callback.message.answer(
        f"🔔 Надіслано нагадування: {count}"
    )

    await callback.answer()
