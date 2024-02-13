"""Модуль запроса подтверждения."""
from aiogram import types
from aiogram.fsm.context import FSMContext

from keyboards.inline.confirm_yes_no import conf_yes_no_button
# from loader import dp


# @dp.callback_query_handler(
#     lambda callback_query: callback_query.data.startswith("confirm_yes_no")
# )
async def confirm_yes_no(
    message: [types.CallbackQuery, types.Message], state: FSMContext
) -> None:
    """
    Функция confirm_yes_no. Коллбэк с датой confirm_yes_no запускает данную функцию.
    Выводит клавиатуру подтверждения действия (Да/Нет).
    """
    data = message.data.split("=")

    kb = conf_yes_no_button(
        callback_yes=f"{data[1]}={data[2]}={data[3]}", callback_no="admin_menu"
    )
    await message.message.answer("Подтвердите:", reply_markup=kb)
    await state.clear()
