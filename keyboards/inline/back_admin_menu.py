"""Модуль создания клавиатуры."""
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def back_admin_menu_button() -> InlineKeyboardMarkup:
    """
    Функция создания клавиатуры для возврата в меню админа
    :return: InlineKeyboardMarkup
    """
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text="Вернуться в меню админа", callback_data="admin_menu")
    # keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()
    #
    # ikeyboard = InlineKeyboardMarkup(
    #     inline_keyboard=[
    #         [
    #             InlineKeyboardButton(
    #                 text="Вернуться в меню админа", callback_data="admin_menu"
    #             )
    #         ],
    #     ],
    # )
    # return ikeyboard
