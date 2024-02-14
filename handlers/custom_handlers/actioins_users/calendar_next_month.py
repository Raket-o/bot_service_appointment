"""Модуль выводит следующий месяц календаря."""
import datetime

from aiogram import types
from aiogram.types import ReplyKeyboardRemove

from config_data.config import ADMINS_TELEGRAM_ID
from database import database
from keyboards.inline.calendar_v1 import calendar_buttons


async def calendar_next_month(message: [types.CallbackQuery, types.Message]) -> None:
    """Функция calendar_next_month. Обработка коллбэк calendar_next_month=.
    Подменяет текущую дату на начало следующего месяца и выводит календарь.
    Если пользователь админ, добавляет кнопу (Админ меню)."""
    telegram_id = message.from_user.id
    date = datetime.datetime.now()
    date = date.replace(day=1, month=date.month + 1)
    callback_data = message.data.split("=")[1]

    kb = await calendar_buttons(date, callback_data)

    kb.button(text="Мои записи", callback_data=f"view_recordings={telegram_id}")

    if telegram_id in ADMINS_TELEGRAM_ID:
        kb.button(text="Админ меню", callback_data="admin_menu")

    kb.adjust(3, 7)
    kb = kb.as_markup()

    await message.message.answer("Выберите дату:", reply_markup=kb)
    await message.message.delete()