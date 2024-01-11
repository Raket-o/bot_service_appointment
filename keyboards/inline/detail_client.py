"""Модуль создания клавиатуры (работа с пользователем)."""
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def details_client_buttons(telegram_id: int, user_blocked: int) -> InlineKeyboardMarkup:
    """
    Функция создания клавиатуры работа с пользователем
    :return: InlineKeyboardMarkup
    """
    ikeyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    "Просмотреть/удалить записи",
                    callback_data=f"view_recordings={telegram_id}",
                )
            ],
            [
                InlineKeyboardButton(
                    f"{'Разблокировать' if user_blocked else 'Заблокировать'} клиента",
                    callback_data=f"confirm_yes_no=blocked={telegram_id}=un"
                    if user_blocked
                    else f"confirm_yes_no=blocked={telegram_id}=bl",
                )
            ],
            [
                InlineKeyboardButton(
                    "Удалить клиента",
                    callback_data=f"confirm_yes_no=del_user={telegram_id}=null",
                )
            ],
        ],
    )
    return ikeyboard
