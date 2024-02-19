"""Модуль милдваре. Запрещает активность заблокированному пользователю."""
import logging
from typing import Any, Awaitable, Callable, Union

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message

from database import transactions


class WhoHereMiddleware(BaseMiddleware):
    """Класс WhoHereMiddleware. Дочерний класс BaseMiddleware"""

    async def __call__(
            self,
            handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
            event: Union[Message, CallbackQuery],
            data: dict[str, Any]
    ) -> Any:

        user_telegram_id = event.from_user.id
        res = await transactions.user_check(user_telegram_id)

        if res:
            if res[0]:
                await data['bot'].send_message(
                    event.from_user.id,
                    "Вы не можете отправлять сообщения в бота."
                )
            else:
                return await handler(event, data)
        else:
            return await handler(event, data)
