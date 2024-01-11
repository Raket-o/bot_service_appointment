""" Модуль обработки каллбэка с датой operations_students"""
from aiogram import types
from aiogram.dispatcher import FSMContext

from database import database
from keyboards.inline.back_admin_menu import back_admin_menu_button
from keyboards.inline.detail_client import details_client_buttons
from loader import dp


@dp.callback_query_handler(lambda callback_query: callback_query.data == "view_clients")
async def view_clients(
    message: [types.CallbackQuery, types.Message], state: FSMContext
) -> None:
    """
    Функция operations_students. Каллбэка с датой operations_students запускает данную функцию.
    Выводит клавиатуру с действиями по событиям и завершает ожидания состояния.
    """
    lst_clients = database.view_clients()

    if lst_clients:
        for client in lst_clients:
            count_date_rec = database.count_date_rec(client[0])
            last_visit_date = client[4].split()
            last_visit_date = last_visit_date[0].split("-")
            last_visit_date = (
                f"{last_visit_date[2]}-{last_visit_date[1]}-{last_visit_date[0]}"
            )

            kb = details_client_buttons(client[0], client[3])
            await message.message.answer(
                f"""Полное имя: {client[1]}
            Телефон: {client[2] if client[2] else "нет телефона"}
            Статус: {"заблокирован" if client[3] else "разблокирован"}
            Количество записей: {count_date_rec}     
            Последний вход: {last_visit_date}        
        """,
                reply_markup=kb,
            )
    else:
        await message.message.answer("Пока что нет ни одного клиента")

    kb = back_admin_menu_button()
    await message.message.answer("Вернуться в админ в меню?", reply_markup=kb)
    await state.finish()
