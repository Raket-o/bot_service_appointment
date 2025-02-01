"""Модуль обработки времени."""
import datetime

from config_data.config import LOCAL_UTC


async def region_current_datetime():
    """
    Функция region_current_datetime.
    Возвращает региональное время если оно заданно в env. файле,
    иначе возвращает дату-время utc
    """
    current_datetime = datetime.datetime.utcnow()
    region_time = current_datetime

    try:
        if LOCAL_UTC:
            if LOCAL_UTC[0] == "+":
                region_time = current_datetime + datetime.timedelta(hours=int(LOCAL_UTC[1:]))

            elif LOCAL_UTC[0] == "-":
                region_time = current_datetime - datetime.timedelta(hours=int(LOCAL_UTC[1:]))
    except ValueError:
        pass

    return region_time
