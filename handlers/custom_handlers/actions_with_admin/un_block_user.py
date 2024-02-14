"""Модуль разбловировки\блокировки пользователя"""
from aiogram import types

from database import database
from keyboards.inline.admin_buttons import admin_buttons


async def unblocked_user(message: [types.CallbackQuery, types.Message]):
    """
    Функция unblocked_user. Коллбэк с датой "blocked=" запускает данную функцию.
    Функция блокирует или разблокирует пользователя.
    """
    telegram_id = message.data.split("=")[1]
    action = message.data.split("=")[2]
    kb = admin_buttons()

    if action == "bl":
        database.block_unblock_user(telegram_id, action)
        await message.message.answer("Клиент заблокирован", reply_markup=kb)
    else:
        database.block_unblock_user(telegram_id, action)
        await message.message.answer("Клиент разблокирован", reply_markup=kb)
