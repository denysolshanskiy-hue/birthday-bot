from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states.auth_state import AuthState
from services.sheets import (
    find_user_by_name,
    save_telegram_data
)

router = Router()


@router.message(AuthState.waiting_for_name)
async def auth_user(message: Message, state: FSMContext):
    full_name = message.text

    user_data = find_user_by_name(full_name)

    if not user_data:
        await message.answer(
            "Користувача не знайдено. Перевірте ПІБ."
        )
        return

    row = user_data["row"]

    username = message.from_user.username or ""

    if username:
        username = f"@{username}"

    save_telegram_data(
        row=row,
        tg_id=message.from_user.id,
        username=username
    )

    await state.clear()

    await message.answer(
        "Авторизація успішна ✅"
    )