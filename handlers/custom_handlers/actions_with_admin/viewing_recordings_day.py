import datetime

from aiogram import types

from database import database
from keyboards.inline.back_admin_menu import back_admin_menu_button
from keyboards.inline.calendar_v1 import calendar_buttons
from loader import dp


@dp.callback_query_handler(
    lambda callback_query: callback_query.data == "viewing_recordings_day"
)
async def viewing_recordings_day_1(message: [types.CallbackQuery, types.Message]):
    current_date = datetime.datetime.now()
    callback_data = "calendar_viewing_recordings_day"
    telegram_id = message.from_user.id

    kb = await calendar_buttons(current_date, callback_data)
    kb.insert(
        types.InlineKeyboardButton(
            "Мои записи", callback_data=f"view_recordings={telegram_id}"
        )
    )
    kb.insert(types.InlineKeyboardButton("Админ меню", callback_data="admin_menu"))
    await message.message.answer("Введите дату, формат ДД-ММ-ГГГГ", reply_markup=kb)


@dp.callback_query_handler(
    lambda callback_query: callback_query.data.startswith(
        "calendar_viewing_recordings_day"
    )
)
async def viewing_recordings_day_2(message: [types.CallbackQuery, types.Message]):
    selected_date = datetime.datetime.strptime(
        message.data.split("_")[4], "%Y-%m-%d %H:%M:%S.%f"
    )

    res = database.viewing_recordings_day_db(selected_date)

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
