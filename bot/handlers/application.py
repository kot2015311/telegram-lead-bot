import re

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from ..keyboards import main_keyboard, remove_keyboard, service_keyboard
from ..states import LeadForm

router = Router(name="application")

ALLOWED_SERVICES = {
    "Разработка бота",
    "Доработка бота",
    "Консультация",
}


def is_valid_name(name: str) -> bool:
    name = name.strip()
    return 2 <= len(name) <= 50


def is_valid_contact(contact: str) -> bool:
    contact = contact.strip()

    if contact.startswith("@") and len(contact) >= 5:
        return True

    digits = re.sub(r"\D", "", contact)
    return 10 <= len(digits) <= 15


@router.message(Command("cancel"))
@router.message(F.text.casefold() == "отмена")
async def cancel_form(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()

    if current_state is None:
        await message.answer(
            "Сейчас нет активной анкеты.",
            reply_markup=main_keyboard,
        )
        return

    await state.clear()
    await message.answer(
        "Анкета отменена.",
        reply_markup=main_keyboard,
    )


@router.message(F.text == "Оставить заявку")
async def start_form(message: Message, state: FSMContext) -> None:
    await state.set_state(LeadForm.service)
    await message.answer(
        "Выберите услугу:",
        reply_markup=service_keyboard,
    )


@router.message(LeadForm.service)
async def process_service(message: Message, state: FSMContext) -> None:
    service = message.text.strip()

    if service not in ALLOWED_SERVICES:
        await message.answer(
            "Пожалуйста, выберите услугу кнопкой ниже.",
            reply_markup=service_keyboard,
        )
        return

    await state.update_data(service=service)
    await state.set_state(LeadForm.name)

    await message.answer(
        "Введите ваше имя:",
        reply_markup=remove_keyboard,
    )


@router.message(LeadForm.name)
async def process_name(message: Message, state: FSMContext) -> None:
    name = message.text.strip()

    if not is_valid_name(name):
        await message.answer(
            "Имя должно содержать от 2 до 50 символов. Попробуйте ещё раз."
        )
        return

    await state.update_data(name=name)
    await state.set_state(LeadForm.contact)

    await message.answer(
        "Введите ваш контакт:\n"
        "- номер телефона\n"
        "- или username в Telegram, например @username"
    )


@router.message(LeadForm.contact)
async def process_contact(message: Message, state: FSMContext) -> None:
    contact = message.text.strip()

    if not is_valid_contact(contact):
        await message.answer(
            "Некорректный контакт. Введите номер телефона или @username."
        )
        return

    await state.update_data(contact=contact)
    data = await state.get_data()
    await state.clear()

    await message.answer(
        "Спасибо! Ваша заявка принята.\n\n"
        f"Услуга: {data['service']}\n"
        f"Имя: {data['name']}\n"
        f"Контакт: {data['contact']}",
        reply_markup=main_keyboard,
    )