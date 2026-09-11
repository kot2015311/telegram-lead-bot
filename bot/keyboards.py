from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_services_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура с выбором услуг."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🤖 Разработка Telegram-ботов")],
            [KeyboardButton(text="🌐 Создание сайтов")],
            [KeyboardButton(text="💡 Консультация / Другое")],
            [KeyboardButton(text="❌ Отмена")],
        ],
        resize_keyboard=True,
    )


def get_cancel_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура с кнопкой отмены."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="❌ Отмена")],
        ],
        resize_keyboard=True,
    )


def get_main_keyboard() -> ReplyKeyboardMarkup:
    """Главная клавиатура (для команды /start)."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📝 Оставить заявку")],
        ],
        resize_keyboard=True,
    )