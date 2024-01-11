"""Модуль создания клавиатуры подтверждения (Да/Нет)."""
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def conf_yes_no_button(callback_yes: str, callback_no: str) -> InlineKeyboardMarkup:
    """
    Функция создания клавиатуры подтверждения (Да/Нет)
    :return: InlineKeyboardMarkup
    """
    ikeyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton("Да", callback_data=callback_yes)],
            [InlineKeyboardButton("Нет", callback_data=callback_no)],
        ],
    )
    return ikeyboard
