from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from ..keyboards import main_keyboard

router = Router(name="start")


@router.message(CommandStart())
async def handle_start(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(
        "Здравствуйте! Это демонстрационный бот для приёма заявок.\n\n"
        "Нажмите кнопку ниже, чтобы оставить заявку.",
        reply_markup=main_keyboard,
    )