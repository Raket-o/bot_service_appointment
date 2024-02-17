""" Модуль инициализации телеграмм бота"""
import asyncio
import logging
from asyncio import ensure_future, get_event_loop

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext

from config_data.config import BOT_TOKEN
from middlewares.who_here import WhoHereMiddleware
from utils.restart_services import restarting_services


logger = logging.getLogger("logger_info")


async def start_up():
    """Функция start_up. При запуске выводит текст в консоль"""
    logger.info("Bot started")


async def on_shutdown():
    """Функция on_shutdown. При завершении выводит текст в консоль"""
    logger.info("Bot stopped")

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
loop = get_event_loop()
dp = Dispatcher()
