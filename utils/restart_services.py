"""Модуль перезапуска сервисов"""
import asyncio
import datetime

from database import database


async def restarting_services() -> None:
    """
    Функция restarting_services. Каждый день в 8:30 утра перезапускает функции:
    удаляет записи (старше 7 дней), удаляет пользователей
    (которые заходили более полгода назад),
    резервирует выходные дни на 2 месяца и отправляет напоминания о записи
    """
    database.deleting_records_older_7_days()
    database.deletes_old_users()

    while True:
        current_date = datetime.datetime.now()

        if current_date.hour == 8 and current_date.minute == 30:
            database.deleting_records_older_7_days()
            database.deletes_old_users()

            from utils.misc.reminder import reminder
            await reminder(current_date)

        await asyncio.sleep(60)
