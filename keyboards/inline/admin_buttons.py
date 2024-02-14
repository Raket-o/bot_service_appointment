"""Модуль создания клавиатуры"""
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def admin_buttons() -> InlineKeyboardMarkup:
    """
    Функция создания клавиатуры для главного админ меню
    :return: InlineKeyboardMarkup
    """
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text="Список клиентов", callback_data="view_clients")
    keyboard_builder.button(text="Поиск клиента", callback_data="search_client")
    keyboard_builder.button(text="Просмотр записей на день", callback_data="viewing_recordings_day")
    keyboard_builder.button(text="Зарезервировать день", callback_data="reserve_day")
    keyboard_builder.button(text="Общая рассылка на день", callback_data="sending_message")
    keyboard_builder.button(text="Вернуться к календарю", callback_data="start_command=calendar_day")
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()
