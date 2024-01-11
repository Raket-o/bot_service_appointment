""" Модуль запуска телеграмм бота"""
import logging

from aiogram import executor

from database.database import init_db
from handlers.default_heandlers import start
from loader import dp, on_shutdown, start_up
from utils.logging import logger_root


init_db()

executor.start_polling(
    dispatcher=dp, skip_updates=True, on_startup=start_up, on_shutdown=on_shutdown
)
