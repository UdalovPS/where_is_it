import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties

from routers import router
from config import BOT_TOKEN


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def main():
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher(storage=MemoryStorage())  # Для FSM

    dp.include_router(router)

    await bot.delete_webhook(drop_pending_updates=True)  # Пропуск старых сообщений
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())