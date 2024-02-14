"""Модуль поиска клиентов по имя и номеру телефона"""
from aiogram import types
from aiogram.fsm.context import FSMContext

from database import database
from keyboards.inline.back_admin_menu import back_admin_menu_button
from keyboards.inline.detail_client import details_client_buttons
from states.states import ServiceDateState


async def search_client_1(message: types.Message, state: FSMContext):
    """
    Функция search_client_1. Коллбэк с датой search_client запускает данную функцию.
    Просит ввести имя, фамилию или номер телефона
    """
    await message.message.answer("Введите имя, фамилию или номер телефона")
    await state.set_state(ServiceDateState.search_client)


async def search_client_2(
    message: types.Message, state: FSMContext
):
    """
    Функция search_client_2. Ожидает изменение состояние ServiceDateState.search_client.
    Вывод пользователя найденных клиентов по имени, фамилии или номеру телефона.
    """
    input_text = message.text
    lst_clients = database.search_client(input_text)

    if lst_clients:
        for client in lst_clients:
            count_date_rec = database.count_date_rec(client[0])
            last_visit_date = client[4].split()
            last_visit_date = last_visit_date[0].split("-")
            last_visit_date = (
                f"{last_visit_date[2]}-{last_visit_date[1]}-{last_visit_date[0]}"
            )

            kb = details_client_buttons(client[0], client[3])

            await message.answer(
                f"""Полное имя: {client[1]}
    Телефон: {client[2]}
    Статус: {"Заблокирован" if client[3] else "Разблокирован"}
    Количество записей: {count_date_rec}     
    Последний вход: {last_visit_date}        
        """,
                reply_markup=kb,
            )
    else:
        await message.answer("Ни кого не нашёл")

    kb = back_admin_menu_button()
    await message.answer("Вернуться в админ в меню?", reply_markup=kb)
    await state.clear()
