"""Модуль обработки просмотра записей."""
import datetime

from aiogram import types
from aiogram.fsm.context import FSMContext

from database import database
from keyboards.reply.list_button import list_button
# from loader import dp
from states.states import ServiceDateState


# @dp.callback_query_handler(
#     lambda callback_query: callback_query.data.startswith("view_recordings=")
# )
async def view_recordings(message: types.Message, state: FSMContext):
    """Функция view_recordings. Запрашивает в базе записи и выводит их пользователю."""
    telegram_id = message.data.split("=")[1]

    res = database.view_record(telegram_id)

    for_btn = []
    if res:
        for i in res:
            date = datetime.datetime.strptime(i[0], "%Y-%m-%d")
            for_btn.append((0, f"{date.day}-{date.month}-{date.year} в {i[1]}:00"))
    else:
        for_btn.append((0, "Записей ещё нет"))

    for_btn.append((0, "Вернуться"))
    kb = list_button(for_btn)
    await message.message.answer("Удалить запись?", reply_markup=kb)

    await state.set_state(ServiceDateState.service_delete)

    # await ServiceDateState.service_delete.set()
