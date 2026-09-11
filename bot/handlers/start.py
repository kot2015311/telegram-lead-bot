from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from bot.keyboards import get_main_keyboard

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        f"Привет, {message.from_user.first_name}! 👋\n\n"
        "Я бот для приёма заявок. Нажми кнопку ниже, чтобы оставить заявку!",
        reply_markup=get_main_keyboard()
    )