"""Модуль удаление пользователя."""
from aiogram import types

from loader import dp


@dp.callback_query_handler(
    lambda callback_query: callback_query.data == "weekend"
)
async def weekend(callback_query: types.CallbackQuery):
    """
    Функция weekend. Коллбэк с датой weekend запускает данную функцию.
    Выводит сообщение пользователя "Выходной день".
    """
    await callback_query.answer("Выходной день")
