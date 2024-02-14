"""Модуль создания клавиатуры (работа с пользователем)"""
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def details_client_buttons(telegram_id: int, user_blocked: int) -> InlineKeyboardMarkup:
    """
    Функция создания клавиатуры работа с пользователем
    :return: InlineKeyboardMarkup
    """
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text="Просмотреть/удалить записи", callback_data=f"view_recordings={telegram_id}")
    keyboard_builder.button(text=f"{'Разблокировать' if user_blocked else 'Заблокировать'} клиента",
                    callback_data=f"confirm_yes_no=blocked={telegram_id}=un"
                    if user_blocked
                    else f"confirm_yes_no=blocked={telegram_id}=bl",
                )
    keyboard_builder.button(text="Удалить клиента",
                    callback_data=f"confirm_yes_no=del_user={telegram_id}=null")
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()
