import aiosqlite
import csv
from datetime import datetime

DB_PATH = "leads.db"


async def init_db():
    """Создание таблицы заявок, если её ещё нет."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                username TEXT,
                service TEXT NOT NULL,
                name TEXT NOT NULL,
                contact TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        await db.commit()


async def add_lead(user_id: int, username: str | None, service: str, name: str, contact: str):
    """Сохранение новой заявки в базу."""
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """
            INSERT INTO leads (user_id, username, service, name, contact, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (user_id, username, service, name, contact, created_at),
        )
        await db.commit()


async def get_recent_leads(limit: int = 5) -> list[dict]:
    """Получение последних N заявок."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT id, service, name, contact, created_at FROM leads ORDER BY id DESC LIMIT ?",
            (limit,)
        ) as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]


async def export_leads_to_csv(filepath: str = "leads_export.csv") -> str:
    """Выгрузка всех заявок в CSV файл (UTF-8 с BOM для Excel)."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM leads ORDER BY id DESC") as cursor:
            rows = await cursor.fetchall()

    # utf-8-sig нужно для корректного открытия кириллицы в Excel
    with open(filepath, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(["ID", "User ID", "Username", "Услуга", "Имя", "Контакт", "Дата создания"])
        
        for row in rows:
            writer.writerow([
                row["id"],
                row["user_id"],
                row["username"],
                row["service"],
                row["name"],
                row["contact"],
                row["created_at"]
            ])

    return filepath