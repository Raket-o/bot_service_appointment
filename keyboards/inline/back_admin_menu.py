"""Модуль создания клавиатуры."""
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def back_admin_menu_button() -> InlineKeyboardMarkup:
    """
    Функция создания клавиатуры для возврата в меню админа
    :return: InlineKeyboardMarkup
    """
    ikeyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    "Вернуться в меню админа", callback_data="admin_menu"
                )
            ],
        ],
    )
    return ikeyboard
