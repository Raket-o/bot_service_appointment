"""Модуль возврата от списка записей к календарю."""
from aiogram import types
from aiogram.fsm.context import FSMContext

from handlers.default_heandlers.start import start_command


async def service_cancel(
    message: [types.CallbackQuery, types.Message], state: FSMContext
):
    """Функция service_cancel. Ожидает изменения состояния ServiceDateState.service_cancel.
    Сбрасывает состояние и возвращает к календарю."""
    input_text = message.text
    if input_text == "Вернуться":
        await state.clear()
        await start_command(message, state)
