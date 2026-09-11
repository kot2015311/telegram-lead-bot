import asyncio
import logging
import gspread
from datetime import datetime
from bot.config import SPREADSHEET_ID

CREDENTIALS_FILE = "service_account.json"


def _sync_append_lead(spreadsheet_id: str, row_data: list):
    """Синхронная функция записи в Google Таблицу."""
    gc = gspread.service_account(filename=CREDENTIALS_FILE)
    sh = gc.open_by_key(spreadsheet_id)
    worksheet = sh.get_worksheet(0)  # Берем первый лист
    worksheet.append_row(row_data)


async def append_lead_to_sheets(service: str, name: str, contact: str, username: str, user_id: int):
    """Асинхронная обертка для добавления заявки в Google Таблицу."""
    if not SPREADSHEET_ID:
        logging.warning("SPREADSHEET_ID не задан. Пропускаем запись в Google Таблицу.")
        return

    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    row = [created_at, service, name, contact, username, str(user_id)]

    try:
        # Выполняем синхронный gspread в отдельном потоке, чтобы не вешать бота
        await asyncio.to_thread(_sync_append_lead, SPREADSHEET_ID, row)
        logging.info("Заявка успешно отправлена в Google Таблицу!")
    except Exception as e:
        logging.error(f"Ошибка при записи в Google Таблицу: {e}") # Убедись, что тут {e}
        print(f"ПОЛНЫЙ ТЕКСТ ОШИБКИ: {e}") # Добавь эту строку для отладки