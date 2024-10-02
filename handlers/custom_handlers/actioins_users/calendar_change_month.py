"""Модуль подменяет месяц календаря."""
import datetime

from aiogram import types

from config_data.config import ADMINS_TELEGRAM_ID
from keyboards.inline.calendar_v1 import calendar_buttons


async def calendar_change_month(message: [types.CallbackQuery, types.Message]) -> None:
    """Функция calendar_change_month. Обработка коллбэк calendar_change_month=.
    Подменяет текущую дату на начало следующего месяца и выводит календарь.
    Если пользователь админ, добавляет кнопу (Админ меню)."""
    telegram_id = message.from_user.id
    date = message.data.split("=")[2]
    date = datetime.datetime.strptime(date, "%Y-%m-%d")

    if message.data.split("=")[1] == "down":
        try:
            date = date.replace(date.year, date.month - 1, 1)
        except ValueError:
            date = date.replace(date.year - 1, 12, 1)
    else:
        try:
            date = date.replace(date.year, date.month + 1, 1)
        except ValueError:
            date = date.replace(date.year + 1, 1, 1)

    callback_data = message.data.split("=")[3]

    kb = await calendar_buttons(date.date(), callback_data)
    kb.button(text="Мои записи", callback_data=f"view_recordings={telegram_id}")

    if telegram_id in ADMINS_TELEGRAM_ID:
        kb.button(text="Админ меню", callback_data="admin_menu")

    kb.adjust(3, 7)
    kb = kb.as_markup()

    await message.message.answer("Выберите дату:", reply_markup=kb)
    await message.message.delete()
