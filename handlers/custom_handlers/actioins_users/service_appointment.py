"""Модуль записи клиента"""
import datetime

from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from config_data import config
from database import database
from handlers.default_heandlers.start import start_command
from keyboards.reply.list_button import list_button
from keyboards.reply.phone_request import contact_button
from loader import bot
from states.states import ServiceDateState

from config_data.config import ADMINS_TELEGRAM_ID


BEGINNING_WORKING_DAY = config.BEGINNING_WORKING_DAY
END_WORKING_DAY = config.END_WORKING_DAY


async def service_appointment_1(message: types.Message, state: FSMContext):
    """Функция service_appointment_1. Выводит свободное время на день."""
    selected_date = datetime.datetime.strptime(
        message.data.split("_")[2], "%Y-%m-%d %H:%M:%S.%f"
    )
    selected_date = selected_date.replace(hour=0, minute=0, second=0, microsecond=0)
    telegram_id = message.from_user.id

    await message.message.answer(
        f"Выбрана дата: {selected_date.day}-{selected_date.month}-{selected_date.year}"
    )

    res = database.get_date_time_appointment(selected_date)

    if res:
        working_hours = [
            [i, 0] for i in range(BEGINNING_WORKING_DAY, END_WORKING_DAY)
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
            [i, f"{i}:00"] for i in range(BEGINNING_WORKING_DAY, END_WORKING_DAY)
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
            await start_command(message)
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
                    selected_date = context_data.get("selected_date")
                    await state.update_data(
                        {
                            "selected_date": selected_date.replace(hour=int(input_text.split(":")[0]))
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
    selected_date = context_data.get("selected_date")

    res = database.check_date_time_appointment(selected_date)
    if not res:
        database.set_date_time_appointment(contact, selected_date)

        sending_text = f"""Новая запись!!!
    Имя: {contact.last_name if contact.last_name else ""} {contact.first_name if contact.first_name else ""}
    На {selected_date.day}-{selected_date.month}-{selected_date.year} в {selected_date.hour}:00.
    Номер телефона: {contact.phone_number}
        """

        for admin_telegram_id in ADMINS_TELEGRAM_ID:
            await bot.send_message(
                chat_id=admin_telegram_id,
                text=sending_text,
                parse_mode="HTML"
            )

        await message.answer(
            f"""Вы записаны на {selected_date.day}-{selected_date.month}-{selected_date.year} в {selected_date.hour}:00.
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
    await start_command(message)
