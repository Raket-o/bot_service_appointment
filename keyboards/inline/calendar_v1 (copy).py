"""Модуль создания клавиатуры календаря."""
import calendar
import datetime

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

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


async def calendar_buttons(date: datetime, action: str) -> InlineKeyboardBuilder:
    """
    Функция создания клавиатуры календаря.
    :return: InlineKeyboardMarkup
    """
    # current_datetime = datetime.datetime.now()
    # print("===================================calendar_buttonscalendar_buttonscalendar_buttonscalendar_buttonscalendar_buttonscalendar_buttons")
    #
    # keyboard_builder = InlineKeyboardBuilder()
    #
    #
    # if date.month == current_datetime.month:
    #     text_btn = (
    #         ("🍪🎅🎁", "ignore"),
    #         (NAMES_MONTH[date.month], "ignore"),
    #         ("-->", f"calendar_next_month={action}"),
    #     )
    # else:
    #     text_btn = (
    #         ("<--", f"start_command={action}"),
    #         (NAMES_MONTH[date.month], "ignore"),
    #         ("🎉🎁🎄", "ignore"),
    #     )
    #
    # for text in text_btn:
    #     keyboard_builder.button(text=text[0], callback_data=text[1])
    #
    # # keyboard_builder.adjust(7)
    #
    # for day in NAMES_DAYS:
    #     keyboard_builder.button(text=day, callback_data="ignore")
    #
    # obj = calendar.Calendar()
    #
    # day_in_month = [num_day for num_day in obj.itermonthdays(date.year, date.month) if num_day >= date.day]
    # list_weekends = get_list_weekends(start_day=day_in_month[0], end_day=day_in_month[-1], date=date)
    #
    # for _ in range(date.weekday()):
    #     keyboard_builder.button(text=" ", callback_data="ignore")
    #
    # for day_num in obj.itermonthdays(date.year, date.month):
    #     if day_num >= date.day:
    #         if day_num in list_weekends and action == "calendar_day":
    #             keyboard_builder.button(text=str(day_num), callback_data="weekend")
    #         else:
    #             callback_data = f"{action}_{date.replace(day=day_num)}"
    #             keyboard_builder.button(text=str(day_num), callback_data=callback_data)
    #
    # add_count_btn = 7 - len(keyboard_builder.__dict__["_markup"][-1])
    # for _ in range(add_count_btn):
    #     keyboard_builder.button(text=" ", callback_data="ignore")
    #
    # return keyboard_builder
    # return keyboard_builder.as_markup()

    # ikeyboard = InlineKeyboardMarkup(row_width=7)
    # ikeyboard = InlineKeyboardMarkup()

    current_datetime = datetime.datetime.now()

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

    # for text in text_btn:
    # ikeyboard = InlineKeyboardMarkup(
    #     inline_keyboard=[
    #         [
    #         InlineKeyboardButton(text=text[0], callback_data=text[1] for text in text_btn)]
    # ]
    # )

    for text in text_btn:
        ikeyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=text[0], callback_data=text[1])],
            ],
        )




    # ikeyboard = InlineKeyboardMarkup(*(
    #         InlineKeyboardButton(text=text[0], callback_data=text[1])
    #         for text in text_btn)
    #                                  )
    # ikeyboard.add(
    #     *(
    #         InlineKeyboardButton(text=text[0], callback_data=text[1])
    #         for text in text_btn
    #     )
    # )

    # ikeyboard.add(
    #     *(InlineKeyboardButton(text=day, callback_data="ignore") for day in NAMES_DAYS)
    # )

    # obj = calendar.Calendar()
    #
    # day_in_month = [num_day for num_day in obj.itermonthdays(date.year, date.month) if num_day >= date.day]
    # list_weekends = get_list_weekends(start_day=day_in_month[0], end_day=day_in_month[-1], date=date)
    #
    # for _ in range(date.weekday()):
    #     ikeyboard.insert(InlineKeyboardButton(text=" ", callback_data="ignore"))
    #
    # for day_num in obj.itermonthdays(date.year, date.month):
    #     if day_num >= date.day:
    #         if day_num in list_weekends and action == "calendar_day":
    #             ikeyboard.insert(
    #                 InlineKeyboardButton(text=str(day_num), callback_data="weekend")
    #             )
    #         else:
    #             callback_data = f"{action}_{date.replace(day=day_num)}"
    #             ikeyboard.insert(
    #                 InlineKeyboardButton(text=str(day_num), callback_data=callback_data)
    #             )
    #
    # add_count_btn = 7 - len(ikeyboard.values["inline_keyboard"][-1])
    # for _ in range(add_count_btn):
    #     ikeyboard.insert(InlineKeyboardButton(text=" ", callback_data="ignore"))

    return ikeyboard




