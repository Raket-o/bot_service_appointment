"""Модуль создания клавиатуры."""
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def admin_buttons() -> InlineKeyboardMarkup:
    """
    Функция создания клавиатуры для главного админ меню
    :return: InlineKeyboardMarkup
    """
    ikeyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton("Список клиентов", callback_data="view_clients")],
            [InlineKeyboardButton("Поиск клиента", callback_data="search_client")],
            [
                InlineKeyboardButton(
                    "Просмотр записей на день", callback_data="viewing_recordings_day"
                )
            ],
            [InlineKeyboardButton("Зарезервировать день", callback_data="reserve_day")],
            [
                InlineKeyboardButton(
                    "Общая рассылка на день", callback_data="sending_message"
                )
            ],
            [
                InlineKeyboardButton(
                    "Вернуться к календарю", callback_data="start_command=calendar_day"
                )
            ],
        ],
    )
    return ikeyboard
