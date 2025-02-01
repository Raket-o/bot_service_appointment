"""Модуль создания клавиатуры календаря."""
import calendar
import datetime

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils.misc.weekend_reservations import ListWeekends

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


async def calendar_buttons(date: datetime, action: str) -> InlineKeyboardBuilder:
    """
    Функция создания клавиатуры календаря.
    :return: InlineKeyboardMarkup
    """
    keyboard_builder = InlineKeyboardBuilder()

    if action == "del_all_record_day_2":
        action += "="

    current_datetime = datetime.datetime.now()
    year_month = f"{date.year} {NAMES_MONTH[date.month]}"

    text_btn = (
        ("🎉🎁🎉", "ignore")
        if date.month == current_datetime.month and date.year == current_datetime.year
        else ("<--", f"calendar_change_month=down={date}={action}"),

        (year_month, "ignore"),
        ("-->", f"calendar_change_month=up={date}={action}"),
    )

    for text in text_btn:
        keyboard_builder.button(text=text[0], callback_data=text[1])

    for day in NAMES_DAYS:
        keyboard_builder.button(text=day, callback_data="ignore")

    obj = calendar.Calendar()

    weekends_obj = ListWeekends()
    list_weekends = await weekends_obj.get_list_weekends()

    btns = [InlineKeyboardButton(text="-", callback_data="ignore") for _ in range(date.weekday())]

    day_ind = 1
    for day_num in obj.itermonthdays(date.year, date.month):
        if day_num >= date.day:
            if day_ind in list_weekends and action == "calendar_day":
                btns.append(InlineKeyboardButton(text="вых", callback_data="weekend"))
            else:
                callback_data = f"{action}_{date.replace(day=day_num)}"
                btns.append(InlineKeyboardButton(text=str(day_num), callback_data=callback_data))

        if day_ind == 7:
            day_ind = 0
        day_ind += 1

    keyboard_builder.row(*btns, width=7)

    add_count_btn = 7 - len(keyboard_builder.__dict__["_markup"][-1])
    for _ in range(add_count_btn):
        keyboard_builder.button(text="-", callback_data="ignore")

    return keyboard_builder
