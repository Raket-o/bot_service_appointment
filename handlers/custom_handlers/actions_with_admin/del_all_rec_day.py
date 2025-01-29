"""Модуль удаления всех записей на день."""
import datetime

from aiogram import types
from aiogram.fsm.context import FSMContext

from database import transactions
from keyboards.inline.back_admin_menu import back_admin_menu_button
from keyboards.inline.calendar_v1 import calendar_buttons
from keyboards.inline.confirm_yes_no import conf_yes_no_button
from loader import bot


async def del_all_record_day_1(message: [types.CallbackQuery, types.Message]):
    """
    Функция del_all_record_day_1. Коллбэк с датой del_all_record_day запускает данную функцию.
    выводит календарь.
    """
    current_date = datetime.date.today()
    callback_data = "del_all_record_day_2="
    telegram_id = message.from_user.id

    kb = await calendar_buttons(current_date, callback_data)
    kb.button(text="Мои записи", callback_data=f"view_recordings={telegram_id}")
    kb.button(text="Админ меню", callback_data="admin_menu")
    kb.adjust(3, 7)
    kb = kb.as_markup()
    await message.message.answer("Выберите дату:", reply_markup=kb)


async def del_all_record_day_2(message: [types.CallbackQuery, types.Message], state: FSMContext):
    """
    Функция del_all_record_day_2. Коллбэк с датой del_all_record_day_2 запускает данную функцию.
    Ждёт подтверждения на резерв дня.
    """
    date = datetime.datetime.strptime(
        message.data.split("=")[1], "_%Y-%m-%d"
    )
    date = date.date()

    await state.update_data({"date": date})

    kb = conf_yes_no_button(
        callback_yes=f"del_all_record_day={date}", callback_no="admin_menu"
    )

    message_date = f"{date.day}-{date.month}-{date.year}"

    await message.message.answer(
        f"Выбрана дата {message_date}. Удаляю записи?", reply_markup=kb
    )


async def del_all_record_day_3(message: [types.CallbackQuery, types.Message], state: FSMContext):
    """
    Функция del_all_record_day_3. Коллбэк с датой del_all_record_day= запускает данную функцию.
    Резервирует день.
    """
    context_data = await state.get_data()
    date = context_data.get("date")

    res = await transactions.mailing_for_day(date)

    message_date = f"{date.day}-{date.month}-{date.year}"

    await transactions.del_record_all_day(date)
    sending_text = f"Ваша запись на {message_date} аннулирована"

    for client in res:
        await bot.send_message(chat_id=client[0], text=sending_text, parse_mode="HTML")

    kb = back_admin_menu_button()
    await message.message.answer("Записи удалены", reply_markup=kb)
