"""Модуль резервирования выходных дней."""
import datetime

from config_data.config import (
    ADMINS_TELEGRAM_ID,
    BEGINNING_WORKING_DAY,
    END_WORKING_DAY,
    WEEKENDS,
)
from database import database


def weekend_reservations():
    """
    Функция weekend_reservations. Функция определяет на какое число выпадает выходной день
    и резервирует его.
    """
    day_dict = {"Пн": 1, "Вт": 2, "Ср": 3, "Чт": 4, "Пт": 5, "Суб": 6, "Вск": 7}
    now = datetime.date.today()

    num_day = [day_dict.get(weekend) for weekend in WEEKENDS]

    if ADMINS_TELEGRAM_ID:
        for i in range(1, 61):
            weekend_day = now + datetime.timedelta(i)
            if datetime.datetime.isoweekday(weekend_day) in num_day:
                database.reserve_day(
                    ADMINS_TELEGRAM_ID[0],
                    weekend_day,
                    BEGINNING_WORKING_DAY,
                    END_WORKING_DAY,
                )
