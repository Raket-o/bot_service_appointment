"""Модуль массовой рассылки сообщений на выбранный день"""
import datetime

from aiogram import types
from aiogram.fsm.context import FSMContext

from database import transactions
from keyboards.inline.back_admin_menu import back_admin_menu_button
from keyboards.inline.calendar_v1 import calendar_buttons
from keyboards.inline.confirm_yes_no import conf_yes_no_button
from loader import bot
from states.states import ServiceDateState

from database.transactions import datetime_trans_str


async def sending_message_1(message: [types.CallbackQuery, types.Message]) -> None:
    """
    Функция sending_message_1. Коллбэк с датой sending_message запускает данную функцию.
    Выводит календарь.
    """
    current_date = datetime.datetime.now()
    callback_data = "sending_message_2"
    telegram_id = message.from_user.id

    kb = await calendar_buttons(current_date, callback_data)
    kb.button(text="Мои записи", callback_data=f"view_recordings={telegram_id}")
    kb.button(text="Админ меню", callback_data="admin_menu")
    kb.adjust(3, 7)
    kb = kb.as_markup()
    await message.message.answer("Выберите дату:", reply_markup=kb)


async def sending_message_2(
        message: [types.CallbackQuery, types.Message], state: FSMContext
):
    """
    Функция sending_message_2. Коллбэк с датой sending_message_2 запускает данную функцию.
    Запрашивает текст рассылки.
    """
    selected_date = datetime.datetime.strptime(
        message.data.split("_")[3], "%Y-%m-%d %H:%M:%S.%f"
    )
    # selected_date_message = (
    #     f"{selected_date.day}-{selected_date.month}-{selected_date.year}"
    # )

    # from database.transactions import datetime_trans_str
    # selected_date_message = datetime_trans_str(selected_date)

    selected_date = selected_date.replace(hour=0, minute=0, second=0, microsecond=0)


    print("sending_message_2", "=" * 50 , type(selected_date), selected_date)
    await state.update_data({"date": selected_date})


    selected_date_message = (
        f"{selected_date.day}-{selected_date.month}-{selected_date.year}"
    )

    await message.message.answer(
        f"Выбрана дата {selected_date_message}. Введите текс для рассылки"
    )
    await state.set_state(ServiceDateState.mailing_for_day)


async def sending_message_3(
        message: [types.CallbackQuery, types.Message], state: FSMContext
):
    """
    Функция sending_message_3. Ожидает изменение состояния ServiceDateState.mailing_for_day.
    Запрашивает подтверждение (Да/Нет).
    """
    sending_text = message.text
    context_data = await state.get_data()
    date = context_data.get("date")

    kb = conf_yes_no_button(callback_yes="sending_message_3", callback_no="admin_menu")
    await message.answer("Отправляю сообщение?", reply_markup=kb)
    await state.clear()
    await state.update_data({"sending_text": sending_text, "date": date})
    # await state.update_data({"sending_text": sending_text})


async def sending_message_4(
        message: [types.CallbackQuery, types.Message], state: FSMContext
):
    """
    Функция sending_message_4. Коллбэк с датой sending_message_3 запускает данную функцию.
    Производит рассылку клиентам в выбранный день.
    """
    context_data = await state.get_data()
    sending_text, date = context_data.get("sending_text"), context_data.get("date")

    date = datetime_trans_str(date)
    res = transactions.mailing_for_day(date)

    for client in res:
        await bot.send_message(chat_id=client[0], text=sending_text, parse_mode="HTML")

    kb = back_admin_menu_button()
    await message.message.answer("Сообщения отправлены", reply_markup=kb)
