from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
from bot.config import ADMIN_ID
from bot.database import get_recent_leads, export_leads_to_csv

router = Router()

# Защита: этот роутер реагирует ТОЛЬКО на сообщения от админа
router.message.filter(F.from_user.id == ADMIN_ID)


@router.message(Command("admin"))
@router.message(Command("leads"))
async def cmd_admin_leads(message: Message):
    """Просмотр последних 5 заявок."""
    leads = await get_recent_leads(limit=5)
    
    if not leads:
        await message.answer("📭 В базе пока нет заявок.")
        return

    text = "📊 <b>Последние заявки из базы:</b>\n\n"
    for lead in leads:
        text += (
            f"🔹 <b>Заявка #{lead['id']}</b> ({lead['created_at']})\n"
            f"• <b>Услуга:</b> {lead['service']}\n"
            f"• <b>Имя:</b> {lead['name']}\n"
            f"• <b>Контакт:</b> {lead['contact']}\n\n"
        )

    text += "📥 Напишите /export чтобы скачать файл с полной базой."
    await message.answer(text, parse_mode="HTML")


@router.message(Command("export"))
async def cmd_export(message: Message):
    """Выгрузка базы данных в CSV файл."""
    await message.answer("⏳ Формирую файл с заявками...")
    
    filepath = await export_leads_to_csv()
    document = FSInputFile(filepath, filename="Все_заявки.csv")
    
    await message.answer_document(
        document=document,
        caption="📈 Все заявки выгружены! Файл открывается в Excel."
    )