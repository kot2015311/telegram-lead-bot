from bot.google_sheets import append_lead_to_sheets
from aiogram import Router, F, Bot
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command

from bot.states import LeadForm
from bot.keyboards import get_services_keyboard, get_cancel_keyboard
from bot.database import add_lead
from bot.config import ADMIN_ID

# Создаем роутер!
router = Router()


@router.message(F.text == "❌ Отмена")
@router.message(Command("cancel"))
async def cancel_handler(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await message.answer(
        "Заполнение анкеты отменено.",
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(F.text == "📝 Оставить заявку")
async def start_application(message: Message, state: FSMContext):
    await state.set_state(LeadForm.service)
    await message.answer(
        "Выберите услугу, которая вас интересует:",
        reply_markup=get_services_keyboard()
    )


@router.message(LeadForm.service)
async def process_service(message: Message, state: FSMContext):
    await state.update_data(service=message.text)
    await state.set_state(LeadForm.name)
    await message.answer(
        "Как к вам обращаться? (Введите ваше имя)",
        reply_markup=get_cancel_keyboard()
    )


@router.message(LeadForm.name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(LeadForm.contact)
    await message.answer(
        "Оставьте ваш номер телефона или логин Telegram для связи:",
        reply_markup=get_cancel_keyboard()
    )


@router.message(LeadForm.contact)
async def process_contact(message: Message, state: FSMContext, bot: Bot):
    contact = message.text.strip()
    await state.update_data(contact=contact)
    data = await state.get_data()

    service = data.get("service")
    name = data.get("name")
    user_id = message.from_user.id
    username = f"@{message.from_user.username}" if message.from_user.username else "Нет username"
    # 1. Сохраняем в SQLite
    await add_lead(
        user_id=user_id,
        username=username,
        service=service,
        name=name,
        contact=contact
    )

    # 1.5. Сохраняем в Google Таблицу
    await append_lead_to_sheets(
        service=service,
        name=name,
        contact=contact,
        username=username,
        user_id=user_id
    )
    # 1. Сохраняем в SQLite
    await add_lead(
        user_id=user_id,
        username=username,
        service=service,
        name=name,
        contact=contact
    )

    # 2. Уведомляем пользователя
    await message.answer(
        "Спасибо! Ваша заявка успешно принята. Мы свяжемся с вами в ближайшее время.",
        reply_markup=ReplyKeyboardRemove()
    )

    # 3. Отправляем карточку заявки админу
    admin_text = (
        "🔥 <b>Новая заявка!</b>\n\n"
        f"<b>Услуга:</b> {service}\n"
        f"<b>Имя:</b> {name}\n"
        f"<b>Контакт:</b> {contact}\n"
        f"<b>Telegram:</b> {username} (ID: <code>{user_id}</code>)"
    )
    
    try:
        await bot.send_message(
            chat_id=ADMIN_ID,
            text=admin_text,
            parse_mode="HTML"
        )
    except Exception as e:
        print(f"Не удалось отправить уведомление админу: {e}")

    # Очищаем FSM
    await state.clear()