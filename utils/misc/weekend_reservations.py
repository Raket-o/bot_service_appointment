"""Модуль поиска выходных дат."""
import datetime
from typing import Tuple

from config_data.config import WEEKENDS


async def get_list_weekends() -> tuple[int | None, ...]:
    """
    Функция get_list_weekend. Возвращает список выходных дней в цифре.
    """
    day_dict = {"Пн": 1, "Вт": 2, "Ср": 3, "Чт": 4, "Пт": 5, "Суб": 6, "Вск": 7}
    return tuple(day_dict.get(weekend) for weekend in WEEKENDS)
