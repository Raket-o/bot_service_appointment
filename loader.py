""" Модуль инициализации телеграмм бота."""
import logging
from asyncio import get_event_loop

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from config_data.config import BOT_TOKEN

logger = logging.getLogger("logger_info")


async def start_up():
    """Функция start_up. При запуске выводит текст в консоль."""
    logger.info("Bot started")


async def on_shutdown():
    """Функция on_shutdown. При завершении выводит текст в консоль."""
    logger.info("Bot stopped")

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
loop = get_event_loop()
dp = Dispatcher()
