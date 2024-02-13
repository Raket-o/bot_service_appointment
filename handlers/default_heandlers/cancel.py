from aiogram import types
#
# from loader import dp
# from states.states import UserInfoState

# from aiogram import Bot, Dispatcher, F, Router, html
import logging

from aiogram.types import Message, ReplyKeyboardRemove
# from aiogram import F, Router
from aiogram.fsm.context import FSMContext
# from aiogram.filters import Command, CommandStart
# from states.states import ServiceDateState

# cancel_router = Router()


# @cancel_router.message(Command("cancel"))
# @cancel_router.message(F.text.casefold() == "cancel")
async def cancel_handler(message: Message, state: FSMContext) -> None:
    """
    Allow user to cancel any action
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