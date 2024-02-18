"""Модуль обработки просмотра записей."""
import datetime

from aiogram import types
from aiogram.fsm.context import FSMContext

from database import transactions
from keyboards.reply.list_button import list_button
from states.states import ServiceDateState


async def view_recordings(message: types.Message, state: FSMContext):
    """Функция view_recordings. Запрашивает в базе записи и выводит их пользователю."""
    telegram_id = message.data.split("=")[1]
    res = await transactions.view_record(telegram_id)

    for_btn = []
    if res:
        for obj in res:
            date = datetime.datetime.strptime(obj.date[:10], "%Y-%m-%d")
            for_btn.append((0, f"{date.day}-{date.month}-{date.year} в {obj.hour}:00"))
    else:
        for_btn.append((0, "Записей ещё нет"))

    for_btn.append((0, "Вернуться"))
    kb = list_button(for_btn)
    await message.message.answer("Удалить запись?", reply_markup=kb)
    await state.set_state(ServiceDateState.service_delete)

