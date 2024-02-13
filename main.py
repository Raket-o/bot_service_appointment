""" Модуль запуска телеграмм бота"""
import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from config_data.config import BOT_TOKEN
# from handlers.default_heandlers import start
from handlers.routers import register_routers

from loader import on_shutdown, start_up, bot, dp
from utils.logging import logger_root

logger_errors = logging.getLogger("logger_errors")
logger_info = logging.getLogger("logger_info")


# init_db()

# executor.start_polling(
#     dispatcher=dp, skip_updates=True, on_startup=start_up, on_shutdown=on_shutdown
# )
# bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
# dp = Dispatcher()


async def main(bot, dp) -> None:
    # bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)

    # dp = Dispatcher()
    dp.startup.register(start_up)
    dp.shutdown.register(on_shutdown)

    register_routers(dp)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
    asyncio.run(main(bot, dp))
