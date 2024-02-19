""" Модуль запуска телеграмм бота."""
import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from config_data.config import BOT_TOKEN
from database.transactions import init_db
from handlers.routers import register_routers
from loader import on_shutdown, start_up, bot, dp
from middlewares.who_here import WhoHereMiddleware
from utils.restart_services import restarting_services


async def main(bot: Bot, dp: Dispatcher) -> None:
    """Функция main. Запускает бота."""
    dp.startup.register(start_up)
    dp.shutdown.register(on_shutdown)

    dp.message.middleware(WhoHereMiddleware())
    dp.callback_query.middleware(WhoHereMiddleware())

    register_routers(dp)

    await init_db()

    asyncio.ensure_future(restarting_services())

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main(bot, dp))
