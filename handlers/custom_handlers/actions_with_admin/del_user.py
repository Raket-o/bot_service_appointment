"""Модуль удаление пользователя."""
from aiogram import types

from database import database
from keyboards.inline.admin_buttons import admin_buttons
from loader import dp


@dp.callback_query_handler(
    lambda callback_query: callback_query.data.startswith("del_user=")
)
async def delete_user(message: [types.CallbackQuery, types.Message]):
    """
    Функция delete_user. Коллбэк с датой del_user= запускает данную функцию.
    Удаляет пользователя.
    """
    telegram_id = message.data.split("=")[1]
    database.del_user(int(telegram_id))

    kb = admin_buttons()
    await message.message.answer("Клиент удалён", reply_markup=kb)
