""" Модуль инициализации телеграмм бота"""
import asyncio
import logging
from asyncio import ensure_future, get_event_loop

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config_data import config
from middlewares.who_here import WhoHereMiddleware
from utils.restart_services import restarting_services


logger = logging.getLogger("logger_loader")


async def start_up(_):
    """Функция start_up. При запуске выводит текст в консоль"""
    logger.info("Bot started")


async def on_shutdown(_):
    """Функция on_shutdown. При завершении выводит текст в консоль"""
    logger.info("Bot stopped")


bot = Bot(token=config.BOT_TOKEN)
storage = MemoryStorage()
loop = get_event_loop()
dp = Dispatcher(bot=bot, storage=storage, loop=loop)
dp.middleware.setup(WhoHereMiddleware())

from utils.restart_services import restarting_services
asyncio.ensure_future(restarting_services())
