"""Модуль создания клавиатуры календаря."""
import calendar
import datetime

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from utils.misc.weekend_reservations import get_list_weekends

NAMES_DAYS = ("Пн", "Вт", "Ср", "Чт", "Пт", "Суб", "Вск")
NAMES_MONTH = {
    1: "Январь",
    2: "Февраль",
    3: "Март",
    4: "Апрель",
    5: "Май",
    6: "Июнь",
    7: "Июль",
    8: "Август",
    9: "Сентябрь",
    10: "Октябрь",
    11: "Ноябрь",
    12: "Декабрь",
}


async def calendar_buttons(date: datetime, action: str) -> InlineKeyboardMarkup:
    """
    Функция создания клавиатуры календаря.
    :return: InlineKeyboardMarkup
    """
    current_datetime = datetime.datetime.now()

    ikeyboard = InlineKeyboardMarkup(row_width=7)

    if date.month == current_datetime.month:
        text_btn = (
            ("🍪🎅🎁", "ignore"),
            (NAMES_MONTH[date.month], "ignore"),
            ("-->", f"calendar_next_month={action}"),
        )
    else:
        text_btn = (
            ("<--", f"start_command={action}"),
            (NAMES_MONTH[date.month], "ignore"),
            ("🎉🎁🎄", "ignore"),
        )

    ikeyboard.add(
        *(
            InlineKeyboardButton(text=text[0], callback_data=text[1])
            for text in text_btn
        )
    )
    ikeyboard.add(
        *(InlineKeyboardButton(text=day, callback_data="ignore") for day in NAMES_DAYS)
    )

    obj = calendar.Calendar()

    day_in_month = [num_day for num_day in obj.itermonthdays(date.year, date.month) if num_day >= date.day]
    list_weekends = get_list_weekends(start_day=day_in_month[0], end_day=day_in_month[-1], date=date)

    for _ in range(date.weekday()):
        ikeyboard.insert(InlineKeyboardButton(" ", callback_data="ignore"))

    for day_num in obj.itermonthdays(date.year, date.month):
        if day_num >= date.day:
            if day_num in list_weekends and action == "calendar_day":
                ikeyboard.insert(
                    InlineKeyboardButton(str(day_num), callback_data="weekend")
                )
            else:
                callback_data = f"{action}_{date.replace(day=day_num)}"
                ikeyboard.insert(
                    InlineKeyboardButton(str(day_num), callback_data=callback_data)
                )

    add_count_btn = 7 - len(ikeyboard.values["inline_keyboard"][-1])
    for _ in range(add_count_btn):
        ikeyboard.insert(InlineKeyboardButton(" ", callback_data="ignore"))

    return ikeyboard
