"""Модуль перезапуска сервисов."""
import asyncio
import datetime

from config_data.config import LOCAL_UTC, REMINDER_TIME
from database import transactions


async def restarting_services() -> None:
    """
    Функция restarting_services. Каждый день в 8:30 утра перезапускает функции:
    удаляет записи (старше 7 дней), удаляет пользователей
    (которые заходили более полгода назад),
    резервирует выходные дни на 2 месяца и отправляет напоминания о записи.
    """
    await transactions.deleting_records_older_7_days()
    await transactions.deletes_old_users()

    try:
        reminder_time = REMINDER_TIME.split(":")
        reminder_hour = int(reminder_time[0])
        reminder_minute = int(reminder_time[1])

    except (IndexError, ValueError):
        reminder_hour = 8
        reminder_minute = 30

    while True:
        current_datetime = datetime.datetime.utcnow()
        region_time = current_datetime

        try:
            if LOCAL_UTC:
                if LOCAL_UTC[0] == "+":
                    region_time = current_datetime.replace(
                        hour=current_datetime.hour + int(LOCAL_UTC[1])
                    )

                elif LOCAL_UTC[0] == "-":
                    region_time = current_datetime.replace(
                        hour=current_datetime.hour - int(LOCAL_UTC[1])
                    )
        except ValueError:
            pass

        if region_time.hour == reminder_hour and region_time.minute == reminder_minute:
            await transactions.deleting_records_older_7_days()
            await transactions.deletes_old_users()

            from utils.misc.reminder import reminder
            await reminder(region_time)

        await asyncio.sleep(60)
