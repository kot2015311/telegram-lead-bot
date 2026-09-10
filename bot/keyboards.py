from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Оставить заявку")],
    ],
    resize_keyboard=True,
)

service_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Разработка бота")],
        [KeyboardButton(text="Доработка бота")],
        [KeyboardButton(text="Консультация")],
        [KeyboardButton(text="Отмена")],
    ],
    resize_keyboard=True,
)

remove_keyboard = ReplyKeyboardRemove()