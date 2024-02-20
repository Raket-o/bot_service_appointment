"""Модуль создания клавиатуры."""
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def rec_del_button(callback) -> InlineKeyboardMarkup:
    """
    Функция создания клавиатуры для главного админ меню.
    :return: InlineKeyboardMarkup
    """
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text="Удалить", callback_data=callback)
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()
