"""Модуль напоминая о записи"""
import datetime

from loader import bot

from database import transactions


async def reminder(date: datetime) -> None:
    """
    Функция reminder. Напоминания о записи. Запрашивает всех пользователей на сегодня.
    """
    res = await transactions.mailing_for_day(date)

    for user in res:
        await bot.send_message(chat_id=user[0], text=f"Напоминаю. У вас сегодня запись на {user[1]}:00 часов.")
