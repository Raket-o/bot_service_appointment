"""Модуль записи клиента"""
import datetime

from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from config_data import config
from config_data.config import ADMINS_TELEGRAM_ID
from database import transactions
from handlers.default_heandlers.start import start_command
from keyboards.reply.list_button import list_button
from keyboards.reply.phone_request import contact_button
from loader import bot
from states.states import ServiceDateState
from utils.misc.region_datetime import region_current_datetime

BEGINNING_WORKING_DAY = config.BEGINNING_WORKING_DAY
END_WORKING_DAY = config.END_WORKING_DAY


async def service_appointment_1(message: types.Message, state: FSMContext):
    """Функция service_appointment_1. Выводит свободное время на день."""
    selected_date = datetime.datetime.strptime(
        message.data.split("_")[2], "%Y-%m-%d"
    )
    selected_date = selected_date.date()
    telegram_id = message.from_user.id

    await message.message.answer(
        f"Выбрана дата: {selected_date.day}-{selected_date.month}-{selected_date.year}"
    )

    res = await transactions.get_date_time_appointment(selected_date)

    region_time: datetime = await region_current_datetime()
    current_hour = region_time.hour
    beginning_working_day = BEGINNING_WORKING_DAY

    if current_hour > BEGINNING_WORKING_DAY and selected_date == region_time.date():
        beginning_working_day = current_hour + 1

    if res:
        working_hours = [
            [i, 0] for i in range(beginning_working_day, END_WORKING_DAY)
        ]
        for i in res:
            for j in working_hours:
                if i[0] == j[0]:
                    j[1] = -1
                else:
                    if j[1] == 0:
                        j[1] = f"{j[0]}:00"
    else:
        working_hours = [
            [i, f"{i}:00"] for i in range(beginning_working_day, END_WORKING_DAY)
        ]

    working_hours.append([0, "Выбрать другую дату"])
    kb = list_button(working_hours)
    await message.message.answer("Выберите свободное время:", reply_markup=kb)

    await state.update_data(
        {
        "telegram_id": telegram_id,
        "firts_name": message.from_user.first_name,
        "last_name": message.from_user.last_name,
        "selected_date": selected_date,
        "working_hours": working_hours
        }
    )

    await state.set_state(ServiceDateState.service_time)


async def service_appointment_2(
    message: [types.CallbackQuery, types.Message], state: FSMContext
):
    """Функция service_appointment_2. Проверяет введено ли правильно время."""
    flag = False
    try:
        input_text = message.text
        if "Выбрать" in input_text:
            await state.clear()
            await start_command(message, state)
        else:
            context_data = await state.get_data()
            if (
                BEGINNING_WORKING_DAY
                <= int(input_text.split(":")[0])
                <= END_WORKING_DAY -1
            ):
                for i in context_data.get("working_hours"):
                    if i[1] == input_text:
                        flag = True

                if flag:
                    await state.update_data(
                        {
                            "selected_hour": int(input_text.split(":")[0])
                        }
                    )

                    kb = await contact_button()
                    await message.answer(
                        "Нажмите на кнопку ниже, чтобы отправить контакт",
                        reply_markup=kb,
                    )
                    await state.set_state(ServiceDateState.service_cancel)

                else:
                    await message.answer("Это время уже занято. Выберите свободное время из списка.")

            else:
                await message.answer("В это время мы не работаем. Выберите свободное время из списка.")

    except ValueError:
        await message.answer("Выберите свободное время из списка.")


async def service_appointment_3(message: types.Message, state: FSMContext):
    """
    Функция service_appointment_3. Проверяет свободна ли дата и время,
    после записывает клиента и уведомляет его и админов.
    """
    contact = message.contact
    context_data = await state.get_data()
    selected_date, selected_hour = context_data.get("selected_date"), context_data.get("selected_hour")

    res = await transactions.check_date_time_appointment(selected_date, selected_hour)
    if not res and selected_date >= datetime.datetime.now().date():
        await transactions.set_date_time_appointment(contact, selected_date, selected_hour)

        sending_text = f"""Новая запись!!!
    Имя: {contact.last_name if contact.last_name else ""} {contact.first_name if contact.first_name else ""}
    На {selected_date.day}-{selected_date.month}-{selected_date.year} в {selected_hour}:00.
    Номер телефона: {contact.phone_number}
        """

        for admin_telegram_id in ADMINS_TELEGRAM_ID:
            await bot.send_message(
                chat_id=admin_telegram_id,
                text=sending_text,
                parse_mode="HTML"
            )

        await message.answer(
            f"""Вы записаны на {selected_date.day}-{selected_date.month}-{selected_date.year} в {selected_hour}:00.
    Ваш номер {contact.phone_number} был получен.
    Вам перезвонят в течение получаса, для подтверждения записи.
    Спасибо, {contact.last_name if contact.last_name else ""} {contact.first_name if contact.first_name else ""}.
            """,
            reply_markup=ReplyKeyboardRemove(),
        )
    else:
        await message.answer(
            "Что-то пошло не так, Попробуйте ещё раз.",
            reply_markup=ReplyKeyboardRemove(),
        )

    await state.clear()
    await start_command(message, state)
