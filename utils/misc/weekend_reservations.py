"""Модуль поиска выходных дат."""
import datetime

from config_data.config import WEEKENDS


def get_list_weekends(start_day: int, end_day: int, date: datetime) -> list[int]:
    """
    Функция get_list_weekend. Возвращает список выходных дат.
    """
    day_dict = {"Пн": 1, "Вт": 2, "Ср": 3, "Чт": 4, "Пт": 5, "Суб": 6, "Вск": 7}

    delta = end_day - start_day

    num_day = [day_dict.get(weekend) for weekend in WEEKENDS]

    return [(date + datetime.timedelta(i)).day
            for i in range(1, delta + 1)
            if datetime.datetime.isoweekday(date + datetime.timedelta(i)) in num_day]


