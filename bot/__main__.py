import asyncio
import logging

from aiogram import Bot, Dispatcher

from .config import load_config
from .handlers.application import router as application_router
from .handlers.start import router as start_router


async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )

    config = load_config()

    dispatcher = Dispatcher()
    dispatcher.include_router(start_router)
    dispatcher.include_router(application_router)

    bot = Bot(token=config.bot_token)
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass