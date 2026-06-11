from keyboards.inline import paid_button

from services.sheets import (
    create_collection,
    collection_exists,
    add_all_participants_to_payments
)
BANK_LINK = "https://send.monobank.ua/jar/6siNn8uvXQ"


async def send_collection(
    bot,
    collection_data
):
    birthday_user = collection_data["birthday_user"]

    participants = collection_data["participants"]

    amount = collection_data["amount"]

    if collection_exists(birthday_user["ПІБ"], birthday_user["ДН"]):
        print(f"Збір для {birthday_user['ПІБ']} вже існує.")
        return

    collection_id = create_collection(
    birthday_name=birthday_user["ПІБ"],
    birthday_date=birthday_user["ДН"],
    amount=amount,
    participants=[
        participant["TG_ID"]
        for participant in participants
    ]
)
    
    # Додати всіх учасників до payments з порожнім paid_at
    add_all_participants_to_payments(
        collection_id,
        birthday_user["ПІБ"]
    )

    text = (
        f"😻Привіт, котики🎉 Через 2 дні день народження у "
        f"{birthday_user['ПІБ']}\n\n"
        f"Сума збору: {amount} грн\n\n"
        f"{BANK_LINK}"
    )

    for user in participants:
        try:
            await bot.send_message(
                chat_id=user["TG_ID"],
                text=text,
                reply_markup=paid_button(collection_id)
            )

        except Exception as e:
            print(
                f"Помилка надсилання "
                f"{user['ПІБ']}: {e}"
            )
