from aiogram import types

from database import database
from keyboards.inline.admin_buttons import admin_buttons
# from loader import dp


# @dp.callback_query_handler(
#     lambda callback_query: callback_query.data.startswith("blocked=")
# )
async def unblocked_user(message: [types.CallbackQuery, types.Message]):
    telegram_id = message.data.split("=")[1]
    action = message.data.split("=")[2]
    kb = admin_buttons()

    if action == "bl":
        database.block_unblock_user(telegram_id, action)
        await message.message.answer("Клиент заблокирован", reply_markup=kb)
    else:
        database.block_unblock_user(telegram_id, action)
        await message.message.answer("Клиент разблокирован", reply_markup=kb)
