"""Модуль создания клавиатуры."""
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def back_admin_menu_button() -> InlineKeyboardMarkup:
    """
    Функция создания клавиатуры для возврата в меню админа.
    :return: InlineKeyboardMarkup
    """
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text="Вернуться в меню админа", callback_data="admin_menu")
    return keyboard_builder.as_markup()
