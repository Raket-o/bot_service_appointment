"""Модуль обработки удаление записи."""
from aiogram import types
from aiogram.dispatcher import FSMContext

from database import database
from handlers.default_heandlers.start import start_command
from keyboards.reply.list_button import list_button
from loader import dp
from states.states import ServiceDateState


@dp.message_handler(state=ServiceDateState.service_delete)
async def delete_recordings_1(
    message: [types.CallbackQuery, types.Message], state: FSMContext
):
    """Функция delete_recordings_1. Ожидает подтверждения на удаление записи."""
    input_text = message.text
    if "Вернуться" in input_text:
        await state.finish()
        await start_command(message)
    else:
        split_text = input_text.split()
        hour = split_text[2].split(":")[0]
        date = split_text[0].split("-")
        date = date[::-1]
        date = "-".join(date)

        async with state.proxy() as data:
            data["date"] = date
            data["hour"] = hour

        for_btn = [(0, "Удалить"), (0, "Вернуться")]
        kb = list_button(for_btn)
        await message.answer("Точно удаляю?", reply_markup=kb)
        await ServiceDateState.service_delete_conf.set()


@dp.message_handler(state=ServiceDateState.service_delete_conf)
async def delete_recordings_2(
    message: [types.CallbackQuery, types.Message], state: FSMContext
):
    """Функция delete_recordings_2. Удаляет запись."""
    input_text = message.text

    if "Вернуться" in input_text:
        await state.finish()
        await start_command(message)
    else:
        async with state.proxy() as data:
            date = data["date"]
            hour = data["hour"]

        database.del_record(date, hour)
        await state.finish()
        await start_command(message)
