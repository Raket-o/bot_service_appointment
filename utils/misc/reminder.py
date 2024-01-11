"""Модуль напоминая о записи"""
import datetime

from database import database
from loader import bot


async def reminder(date: datetime) -> None:
    """
    Функция reminder. Напоминания о записи. Запрашивает всех пользователей на сегодня.
    """
    res = database.mailing_for_day(date)

    for user in res:
        await bot.send_message(chat_id=user[0], text="Напоминаю. У вас сегодня запись.")
