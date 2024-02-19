"""Модуль вывода пользователей записанных на определённый день."""
import datetime

from aiogram import types

from database import transactions
from keyboards.inline.back_admin_menu import back_admin_menu_button
from keyboards.inline.calendar_v1 import calendar_buttons


async def viewing_recordings_day_1(message: [types.CallbackQuery, types.Message]):
    """
    Функция view_clients. Коллбэк с датой view_rec_client= запускает данную функцию.
    Запрашивает дату для выводи записей пользователя.
    """
    current_date = datetime.datetime.now()
    callback_data = "calendar_viewing_recordings_day"
    telegram_id = message.from_user.id

    kb = await calendar_buttons(current_date, callback_data)
    kb.button(text="Мои записи", callback_data=f"view_recordings={telegram_id}")
    kb.button(text="Админ меню", callback_data="admin_menu")
    kb.adjust(3, 7)
    kb = kb.as_markup()
    await message.message.answer("Введите дату, формат ДД-ММ-ГГГГ", reply_markup=kb)


async def viewing_recordings_day_2(message: [types.CallbackQuery, types.Message]):
    """
    Функция viewing_recordings_day_2. Коллбэк с датой calendar_viewing_recordings_day запускает данную функцию.
    Функция выводит пользователей записанных на определённый день.
    """
    selected_date = datetime.datetime.strptime(
        message.data.split("_")[4], "%Y-%m-%d %H:%M:%S.%f"
    )
    selected_date = selected_date.date()

    res = await transactions.viewing_recordings_day_db(selected_date)

    if res:
        for user in res:
            await message.message.answer(
                f"""Клиент: {user[0]}
        Телефон: {user[1]}
        Записан на {user[2]} часов
        """
            )
    else:
        await message.message.answer("На этот день нет записей")

    kb = back_admin_menu_button()
    await message.message.answer("Запрос выполнил", reply_markup=kb)
