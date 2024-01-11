"""Модуль конфиг для проверки создано ли окружение."""
import os

from dotenv import find_dotenv, load_dotenv

if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
START_MESSAGE = os.getenv("START_MESSAGE")
BEGINNING_WORKING_DAY = int(os.getenv("BEGINNING_WORKING_DAY"))
END_WORKING_DAY = int(os.getenv("END_WORKING_DAY"))
ADMINS_TELEGRAM_ID = [int(i) for i in os.getenv("ADMINS_TELEGRAM_ID").split()]
WEEKENDS = [i.capitalize() for i in os.getenv("WEEKENDS").split()]

DEFAULT_COMMANDS = ("start", "Запустить бота")
