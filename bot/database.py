import aiosqlite
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