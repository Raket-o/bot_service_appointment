"""Модуль вывода пользователей записанных на определённый день."""
import datetime

from aiogram import types

from database import transactions
from keyboards.inline.back_admin_menu import back_admin_menu_button
from keyboards.inline.calendar_v1 import calendar_buttons
from keyboards.inline.rec_del import rec_del_button


async def viewing_recordings_day_1(message: [types.CallbackQuery, types.Message]):
    """
    Функция view_clients. Коллбэк с датой view_rec_client= запускает данную функцию.
    Запрашивает дату для выводи записей пользователя.
    """
    current_date = datetime.datetime.now()
    current_date = current_date.date()
    callback_data = "view_recs_day"
    telegram_id = message.from_user.id

    kb = await calendar_buttons(current_date, callback_data)
    kb.button(text="Мои записи", callback_data=f"view_recordings={telegram_id}")
    kb.button(text="Админ меню", callback_data="admin_menu")
    kb.adjust(3, 7)
    kb = kb.as_markup()
    await message.message.answer("Выберите дату:", reply_markup=kb)


async def viewing_recordings_day_2(message: [types.CallbackQuery, types.Message]):
    """
    Функция viewing_recordings_day_2. Коллбэк с датой calendar_viewing_recordings_day запускает данную функцию.
    Функция выводит пользователей записанных на определённый день.
    """
    selected_date = datetime.datetime.strptime(
        message.data.split("_")[3], "%Y-%m-%d"
    )
    selected_date = selected_date.date()

    res = await transactions.viewing_recordings_day_db(selected_date)

    if res:
        for user in res:
            callback_rec_del_button = f"confirm_yes_no=rec_del_with_day={selected_date}={user[2]}"
            kb_rec_del = rec_del_button(callback_rec_del_button)
            await message.message.answer(
                f"""Клиент: {user[0]}
        Телефон: {user[1]}
        Записан на {user[2]} часов
        """,
                reply_markup=kb_rec_del
            )
    else:
        await message.message.answer("На этот день нет записей")

    kb = back_admin_menu_button()
    await message.message.answer("Запрос выполнил", reply_markup=kb)
