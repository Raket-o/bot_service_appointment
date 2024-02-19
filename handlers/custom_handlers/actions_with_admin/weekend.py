"""Модуль сообщает пользовалю о выходном дне."""
from aiogram import types


async def weekend(callback_query: types.CallbackQuery):
    """
    Функция weekend. Коллбэк с датой weekend запускает данную функцию.
    Выводит сообщение пользователя "Выходной день".
    """
    await callback_query.answer("Выходной день")
