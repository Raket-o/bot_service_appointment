"""Модуль резервирования дня."""
import datetime

from aiogram import types
from aiogram.fsm.context import FSMContext

from config_data import config
from database import transactions
from keyboards.inline.back_admin_menu import back_admin_menu_button
from keyboards.inline.calendar_v1 import calendar_buttons
from keyboards.inline.confirm_yes_no import conf_yes_no_button
from loader import bot

from database.transactions import datetime_trans_str


async def reserve_day_1(message: [types.CallbackQuery, types.Message]):
    """
    Функция reserve_day_1. Коллбэк с датой reserve_day запускает данную функцию.
    выводит календарь.
    """
    current_date = datetime.datetime.now()
    callback_data = "reserve_day_2"
    telegram_id = message.from_user.id

    kb = await calendar_buttons(current_date, callback_data)
    kb.button(text="Мои записи", callback_data=f"view_recordings={telegram_id}")
    kb.button(text="Админ меню", callback_data="admin_menu")
    kb.adjust(3, 7)
    kb = kb.as_markup()
    await message.message.answer("Выберите дату:", reply_markup=kb)


async def reserve_day_2(message: [types.CallbackQuery, types.Message], state: FSMContext):
    """
    Функция reserve_day_2. Коллбэк с датой reserve_day_2 запускает данную функцию.
    Ждёт подтверждения на резерв дня.
    """
    selected_date = datetime.datetime.strptime(
        message.data.split("_")[3], "%Y-%m-%d %H:%M:%S.%f"
    )

    selected_date_message = (datetime_trans_str(selected_date))

    await state.update_data({"date": selected_date_message})

    kb = conf_yes_no_button(
        callback_yes=f"reserve_day={selected_date}", callback_no="admin_menu"
    )
    await message.message.answer(
        f"Выбрана дата {selected_date_message}. Резервирую день?", reply_markup=kb
    )


async def reserve_day_3(message: [types.CallbackQuery, types.Message], state: FSMContext):
    """
    Функция reserve_day_3. Коллбэк с датой reserve_day= запускает данную функцию.
    Резервирует день.
    """
    telegram_id = message.from_user.id
    context_data = await state.get_data()
    date = context_data.get("date")
    res = transactions.mailing_for_day(date)

    date = datetime.datetime.strptime(date, "%Y-%m-%d")

    sending_text = f"Ваша запись на {date.day}-{date.month}-{date.year} аннулирована"

    for client in res:
        await bot.send_message(chat_id=client[0], text=sending_text, parse_mode="HTML")

    date = f"{date.year}-{date.month}-{date.day}"

    transactions.reserve_day(
        telegram_id, date, config.BEGINNING_WORKING_DAY, config.END_WORKING_DAY
    )

    kb = back_admin_menu_button()
    await message.message.answer("День зарезервирован", reply_markup=kb)
