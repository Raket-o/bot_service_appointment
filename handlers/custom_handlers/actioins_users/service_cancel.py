"""Модуль возврата от списка записей к календарю."""
from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.default_heandlers.start import start_command
from loader import dp
from states.states import ServiceDateState


@dp.message_handler(state=ServiceDateState.service_cancel)
async def service_cancel(
    message: [types.CallbackQuery, types.Message], state: FSMContext
):
    """Функция service_cancel. Ожидает изменения состояния ServiceDateState.service_cancel.
    Сбрасывает состояние и возвращает к календарю."""
    input_text = message.text
    if input_text == "Вернуться":
        await state.finish()
        await start_command(message)
