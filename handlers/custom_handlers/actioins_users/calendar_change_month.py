"""Модуль подменяет месяц календаря."""
import datetime

from aiogram import types
from aiogram.fsm.context import FSMContext

from config_data.config import ADMINS_TELEGRAM_ID
from keyboards.inline.calendar_v1 import calendar_buttons
from utils.calendar import InternalCalendar


async def calendar_change_month(message: [types.CallbackQuery, types.Message], state: FSMContext) -> None:
    """Функция calendar_change_month. Обработка коллбэк calendar_change_month=.
    Подменяет текущую дату на начало следующего месяца и выводит календарь.
    Если пользователь админ, добавляет кнопу (Админ меню)."""
    context_data = await state.get_data()

    if not context_data:
        await state.update_data({"user_calen": InternalCalendar(message.from_user.id)})
        context_data = await state.get_data()

    user_calen: InternalCalendar = context_data.get("user_calen")

    if message.data.split("=")[1] == "down":
        date = await user_calen.pre_month()
    else:
        date = await user_calen.next_month()

    callback_data = message.data.split("=")[3]

    kb = await calendar_buttons(date, callback_data)
    kb.button(text="Мои записи", callback_data=f"view_recordings={user_calen.telegram_id}")

    if user_calen.telegram_id in ADMINS_TELEGRAM_ID:
        kb.button(text="Админ меню", callback_data="admin_menu")

    kb.adjust(3, 7)
    kb = kb.as_markup()

    await message.message.answer("Выберите дату:", reply_markup=kb)
    await message.message.delete()
