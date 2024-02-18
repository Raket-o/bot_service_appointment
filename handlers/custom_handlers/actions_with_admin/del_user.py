"""Модуль удаление пользователя."""
from aiogram import types

from database import transactions
from keyboards.inline.admin_buttons import admin_buttons


async def delete_user(message: [types.CallbackQuery, types.Message]):
    """
    Функция delete_user. Коллбэк с датой del_user= запускает данную функцию.
    Удаляет пользователя.
    """
    telegram_id = message.data.split("=")[1]
    await transactions.del_user(int(telegram_id))

    kb = admin_buttons()
    await message.message.answer("Клиент удалён", reply_markup=kb)
