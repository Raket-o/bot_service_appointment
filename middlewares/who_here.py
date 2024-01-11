"""Модуль милдваре. Запрещает активность заблокированному пользователю"""
import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware

from config_data.config import ADMINS_TELEGRAM_ID
from database import database

logger = logging.getLogger("logger_middleware")


class WhoHereMiddleware(BaseMiddleware):
    """Класс WhoHereMiddleware. Дочерний класс BaseMiddleware"""

    async def on_pre_process_update(self, update: types.Update, data: dict):
        """
        Функция on_pre_process_update. Перехватывает ивенты от пользователей
        и если он заблокирован, выводи текст о блокировке
        """
        try:
            user_telegram_id = int(update.message.from_user.id)

        except (NameError, AttributeError):
            user_telegram_id = int(update["callback_query"]["from"]["id"])

        res = database.user_check(user_telegram_id)

        if res:
            if res[0]:
                if update["callback_query"]:
                    await update.callback_query.answer(
                        "Вы не можете отправлять сообщения в бота."
                    )
                elif update["message"]:
                    await update.message.answer(
                        "Вы не можете отправлять сообщения в бота."
                    )
                raise CancelHandler()
