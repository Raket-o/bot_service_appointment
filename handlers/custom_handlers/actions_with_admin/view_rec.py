import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext

from database import database
from keyboards.reply.list_button import list_button
from loader import dp


@dp.callback_query_handler(
    lambda callback_query: callback_query.data.startswith("view_rec_client=")
)
async def view_rec(message: [types.CallbackQuery, types.Message], state: FSMContext):
    telegram_id = message.data.split("=")[1]
    res = database.view_client_records(telegram_id)

    if res:
        list_to_btn = []
        for i in res:
            date_rec = datetime.datetime.strptime(i[0], "%Y-%m-%d")
            list_to_btn.append(
                (0, f"{date_rec.day}-{date_rec.month}-{date_rec.year} в {i[1]} часов")
            )
    else:
        await message.message.answer("Нет у него ни одной записи")

    kb = list_button(list_to_btn)
    kb.insert("Удалить все записи")
    kb.insert("Вернуться назад")
    await message.message.answer("Что-то хотите удалить?", reply_markup=kb)
    await state.finish()
