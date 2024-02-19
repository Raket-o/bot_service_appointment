"""Модуль вывода всех пользователей."""
from aiogram import types
from aiogram.fsm.context import FSMContext

from database import transactions
from keyboards.inline.back_admin_menu import back_admin_menu_button
from keyboards.inline.detail_client import details_client_buttons


async def view_clients(
    message: [types.CallbackQuery, types.Message], state: FSMContext
) -> None:
    """
    Функция view_clients. Коллбэк с датой view_clients запускает данную функцию.
    Вывод всех пользователей.
    """
    lst_clients = await transactions.view_clients()

    if lst_clients:
        for client in lst_clients:
            count_date_rec = await transactions.count_date_rec(client[0].telegramm_id)
            last_visit_date = client[0].last_visit_date.split()
            last_visit_date = last_visit_date[0].split("-")
            last_visit_date = (
                f"{last_visit_date[2]}-{last_visit_date[1]}-{last_visit_date[0]}"
            )

            kb = details_client_buttons(client[0].telegramm_id, client[0].blocked)
            await message.message.answer(
                f"""Полное имя: {client[0].full_name}
            Телефон: {client[0].telephone if client[0].telephone else "нет телефона"}
            Статус: {"заблокирован" if client[0].blocked else "разблокирован"}
            Количество записей: {count_date_rec[0]}     
            Последний вход: {last_visit_date}        
        """,
                reply_markup=kb,
            )
    else:
        await message.message.answer("Пока что нет ни одного клиента")

    kb = back_admin_menu_button()
    await message.message.answer("Вернуться в админ в меню?", reply_markup=kb)
    await state.clear()
