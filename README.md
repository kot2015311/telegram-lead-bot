# Telegram Lead Bot

Демонстрационный Telegram-бот для приёма заявок на услуги.

## Функции
- Команда `/start`
- Кнопка **Оставить заявку**
- Анкета через FSM
- Выбор услуги
- Проверка имени и контакта
- Отмена анкеты через `/cancel` или кнопку **Отмена**

## Стек
- Python 3.12
- aiogram 3
- python-dotenv

## Структура проекта
```text
bot/
  handlers/
    application.py
    start.py
  __main__.py
  config.py
  keyboards.py
  states.py