"""Модуль создания клавиатуры подтверждения (Да/Нет)."""
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def conf_yes_no_button(callback_yes: str, callback_no: str) -> InlineKeyboardMarkup:
    """
    Функция создания клавиатуры подтверждения (Да/Нет).
    :return: InlineKeyboardMarkup
    """
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text="Да", callback_data=callback_yes)
    keyboard_builder.button(text="Нет", callback_data=callback_no)
    keyboard_builder.adjust(2)
    return keyboard_builder.as_markup()
