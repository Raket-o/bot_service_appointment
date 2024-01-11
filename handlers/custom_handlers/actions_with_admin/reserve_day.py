"""Модуль резервирования дня."""
import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext

from config_data import config
from database import database
from keyboards.inline.back_admin_menu import back_admin_menu_button
from keyboards.inline.calendar_v1 import calendar_buttons
from keyboards.inline.confirm_yes_no import conf_yes_no_button
from loader import bot, dp


@dp.callback_query_handler(lambda callback_query: callback_query.data == "reserve_day")
async def reserve_day_1(message: [types.CallbackQuery, types.Message]):
    """
    Функция reserve_day_1. Коллбэк с датой reserve_day запускает данную функцию.
    выводит календарь.
    """
    current_date = datetime.datetime.now()
    callback_data = "reserve_day_2"
    telegram_id = message.from_user.id

    kb = await calendar_buttons(current_date, callback_data)
    kb.insert(
        types.InlineKeyboardButton(
            "Мои записи", callback_data=f"view_recordings={telegram_id}"
        )
    )
    kb.insert(types.InlineKeyboardButton("Админ меню", callback_data="admin_menu"))
    await message.message.answer("Выберите дату:", reply_markup=kb)


@dp.callback_query_handler(
    lambda callback_query: callback_query.data.startswith("reserve_day_2")
)
async def reserve_day_2(message: [types.CallbackQuery, types.Message]):
    """
    Функция reserve_day_2. Коллбэк с датой reserve_day_2 запускает данную функцию.
    Ждёт подтверждения на резерв дня.
    """
    selected_date = datetime.datetime.strptime(
        message.data.split("_")[3], "%Y-%m-%d %H:%M:%S.%f"
    )
    selected_date_message = (
        f"{selected_date.day}-{selected_date.month}-{selected_date.year}"
    )

    kb = conf_yes_no_button(
        callback_yes=f"reserve_day={selected_date}", callback_no="admin_menu"
    )
    await message.message.answer(
        f"Выбрана дата {selected_date_message}. Резервирую день?", reply_markup=kb
    )


@dp.callback_query_handler(
    lambda callback_query: callback_query.data.startswith("reserve_day=")
)
async def reserve_day_3(message: [types.CallbackQuery, types.Message]):
    """
    Функция reserve_day_3. Коллбэк с датой reserve_day= запускает данную функцию.
    Резервирует день.
    """
    data = message.data.split("=")
    telegram_id = int(message["from"]["id"])
    date = data[1].split()[0]
    date = datetime.datetime.strptime(date, "%Y-%m-%d")

    res = database.mailing_for_day(date)

    sending_text = f"Ваша запись на {date.day}-{date.month}-{date.year} аннулирована"

    for client in res:
        await bot.send_message(chat_id=client[0], text=sending_text, parse_mode="HTML")

    database.reserve_day(
        telegram_id, date, config.BEGINNING_WORKING_DAY, config.END_WORKING_DAY
    )

    kb = back_admin_menu_button()
    await message.message.answer("День зарезервирован", reply_markup=kb)
