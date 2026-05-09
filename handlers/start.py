from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from states.auth_state import AuthState
import os

from dotenv import load_dotenv

from keyboards.reply import (
    admin_keyboard
)
from services.sheets import (
    user_already_registered
)

load_dotenv()
ADMIN_ID = os.getenv("ADMIN_ID")
router = Router()


@router.message(CommandStart())
async def start_handler(
    message: Message,
    state: FSMContext
):
    if user_already_registered(
        message.from_user.id
    ):
        if str(message.from_user.id) == ADMIN_ID:
            await message.answer(
                "Адмін меню 👇",
                reply_markup=admin_keyboard
            )

        else:
            await message.answer(
                "Ви вже авторизовані ✅"
            )

        return

    await state.set_state(
        AuthState.waiting_for_name
    )

    await message.answer(
        "Введіть ваше ПІБ для авторизації."
    )