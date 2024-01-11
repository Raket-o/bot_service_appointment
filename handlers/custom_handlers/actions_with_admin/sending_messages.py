""" Модуль массовой рассылки сообщений на выбранный день"""
import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext

from database import database
from keyboards.inline.back_admin_menu import back_admin_menu_button
from keyboards.inline.calendar_v1 import calendar_buttons
from keyboards.inline.confirm_yes_no import conf_yes_no_button
from loader import bot, dp
from states.states import ServiceDateState


@dp.callback_query_handler(
    lambda callback_query: callback_query.data == "sending_message"
)
async def sending_message_1(message: [types.CallbackQuery, types.Message]) -> None:
    """
    Функция sending_message_1. Коллбэк с датой sending_message запускает данную функцию.
    Выводит календарь.
    """
    current_date = datetime.datetime.now()
    callback_data = "sending_message_2"
    telegram_id = message.from_user.id

    kb = await calendar_buttons(current_date, callback_data)
    kb.insert(
        types.InlineKeyboardButton(
            "Мои записи", callback_data=f"view_recordings={telegram_id}"
        )
    )
    kb.insert(types.InlineKeyboardButton("Админ меню", callback_data="admin_menu"))
    await message.message.answer("Выберите дату:", reply_markup=kb)


@dp.callback_query_handler(
    lambda callback_query: callback_query.data.startswith("sending_message_2")
)
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
    selected_date_message = (
        f"{selected_date.day}-{selected_date.month}-{selected_date.year}"
    )

    async with state.proxy() as data:
        data["date"] = selected_date

    await message.message.answer(
        f"Выбрана дата {selected_date_message}. Введите текс для рассылки"
    )
    await ServiceDateState.mailing_for_day.set()


@dp.message_handler(state=ServiceDateState.mailing_for_day)
async def sending_message_3(
    message: [types.CallbackQuery, types.Message], state: FSMContext
):
    """
    Функция sending_message_3. Ожидает изменение состояния ServiceDateState.mailing_for_day.
    Запрашивает подтверждение (Да/Нет).
    """
    sending_text = message.text

    async with state.proxy() as data:
        date = data["date"]

    kb = conf_yes_no_button(callback_yes="sending_message_3", callback_no="admin_menu")
    await message.answer("Отправляю сообщение?", reply_markup=kb)
    await state.finish()

    async with state.proxy() as data:
        data["sending_text"] = sending_text
        data["date"] = date


@dp.callback_query_handler(
    lambda callback_query: callback_query.data == "sending_message_3"
)
async def sending_message_4(
    message: [types.CallbackQuery, types.Message], state: FSMContext
):
    """
    Функция sending_message_4. Коллбэк с датой sending_message_3 запускает данную функцию.
    Производит рассылку клиентам в выбранный день.
    """
    async with state.proxy() as data:
        sending_text = data["sending_text"]
        date = data["date"]

    res = database.mailing_for_day(date)

    for client in res:
        await bot.send_message(chat_id=client[0], text=sending_text, parse_mode="HTML")

    kb = back_admin_menu_button()
    await message.message.answer("Сообщения отправлены", reply_markup=kb)
