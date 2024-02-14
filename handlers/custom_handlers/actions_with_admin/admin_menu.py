"""Модуль админ меню."""
from aiogram import types
from aiogram.fsm.context import FSMContext

from keyboards.inline.admin_buttons import admin_buttons


async def admin_menu(
    message: [types.CallbackQuery, types.Message], state: FSMContext
) -> None:
    """
    Функция admin_menu. Коллбэк с датой admin_menu запускает данную функцию.
    Выводит клавиатуру админ меню.
    """
    kb = admin_buttons()
    await message.message.answer("Выберите действие:", reply_markup=kb)
    await state.clear()
    await message.message.delete()
