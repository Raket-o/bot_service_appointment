"""Модуль сброса состояние пользователя."""
from aiogram import types
import logging

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove


async def cancel_handler(message: Message, state: FSMContext) -> None:
    """
    Функция weekend. Команда /cancel запускает данную функцию.
    Функция сбрасывает состояние пользователя.
    """
    logging.info("cancel_handler")

    current_state = await state.get_state()
    if current_state is None:
        await message.answer(
            "Cancelled.",
            reply_markup=ReplyKeyboardRemove(),
        )
        return

    logging.info("Cancelling state %r", current_state)
    await state.clear()
    await message.answer(
        "Cancelled.",
        reply_markup=ReplyKeyboardRemove(),
    )