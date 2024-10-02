"""Модуль выводит следующий месяц календаря."""
import datetime

from aiogram import types

from config_data.config import ADMINS_TELEGRAM_ID
from keyboards.inline.calendar_v1 import calendar_buttons
from utils.calendar import InternalCalendar
# from handlers.default_heandlers.start import
from states.states import ServiceDateState

internal_calendar = InternalCalendar()


async def calendar_change_month(message: [types.CallbackQuery, types.Message]) -> None:
    """Функция calendar_change_month. Обработка коллбэк calendar_next_month=.
    Подменяет текущую дату на начало следующего месяца и выводит календарь.
    Если пользователь админ, добавляет кнопу (Админ меню)."""
    print(message.data.split("="))
    telegram_id = message.from_user.id
    # internal_calendar = Form.calen_1

    if message.data.split("=")[1] == "down":
        date = internal_calendar.previous_month()
    else:
        date = internal_calendar.next_month()
    callback_data = message.data.split("=")[2]

    kb = await calendar_buttons(date, callback_data, internal_calendar.is_previous_month())
    kb.button(text="Мои записи", callback_data=f"view_recordings={telegram_id}")

    if telegram_id in ADMINS_TELEGRAM_ID:
        kb.button(text="Админ меню", callback_data="admin_menu")

    kb.adjust(3, 7)
    kb = kb.as_markup()

    await message.message.answer("Выберите дату:", reply_markup=kb)
    await message.message.delete()
