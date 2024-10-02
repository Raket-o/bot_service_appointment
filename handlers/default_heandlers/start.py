""" Модуль команды /start."""
import datetime
import logging

from aiogram import types
from aiogram.types import ReplyKeyboardRemove

from config_data.config import ADMINS_TELEGRAM_ID, START_MESSAGE
from database import transactions
from keyboards.inline.calendar_v1 import calendar_buttons
from utils.calendar import InternalCalendar

from states.states import ServiceDateState

start_logger = logging.getLogger(__name__)


async def start_command(message: [types.CallbackQuery, types.Message]) -> None:
    """
    Вывод тест START_MESSAGE и календарь.
    Если пользователя админ, то добавляет кнопки админ меню
    """
    try:
        callback_data = message.data.split("=")[1]
    except AttributeError:
        callback_data = "calendar_day"

    telegram_id = message.from_user.id
    full_name = message.from_user.full_name
    res = await transactions.user_check(telegram_id)

    if not res:
        await transactions.add_user(telegram_id, full_name)

    await transactions.update_visit_date(telegram_id)

    # current_date = datetime.datetime.now()
    # current_date = current_date.date()

    # internal_calendar = InternalCalendar()
    current_date = internal_calendar.calen_date
    # internal_calendar = Form.calen_1
    current_date = internal_calendar.calen_date


    kb = await calendar_buttons(current_date, callback_data, internal_calendar.is_previous_month())
    kb.button(text="Мои записи", callback_data=f"view_recordings={telegram_id}")

    if telegram_id in ADMINS_TELEGRAM_ID:
        kb.button(text="Админ меню", callback_data="admin_menu")

    kb.adjust(3, 7)
    kb = kb.as_markup()

    if isinstance(message, types.Message):
        await message.answer(
            START_MESSAGE, parse_mode="HTML", reply_markup=ReplyKeyboardRemove()
        )
        await message.answer(text="Выберите дату:", reply_markup=kb)

    elif isinstance(message, types.CallbackQuery):
        await message.message.answer(text="Выберите дату:", reply_markup=kb)
        await message.message.delete()

    start_logger.info(f"start_logger-UserID={telegram_id} {full_name}")
