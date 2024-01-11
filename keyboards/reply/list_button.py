"""Модуль генерации клавиатуры. Имя берётся из входящего списка."""
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def list_button(lst: list) -> ReplyKeyboardMarkup:
    """
    Функция создания клавиатуры list_button.
    Принимает на вход список где lst[1]: str - названия кнопок,
    (если значение lst[1]= -1, пропускает)
    остальные элементы опциональны.
    :return: ReplyKeyboardMarkup
    """
    keyboard = ReplyKeyboardMarkup(
        resize_keyboard=True, row_width=2, one_time_keyboard=True
    )
    keyboard.add(*(KeyboardButton(i_lst[1]) for i_lst in lst if i_lst[1] != -1))
    return keyboard
