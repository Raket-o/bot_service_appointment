"""Модуль хранения данных (состояний) пользователя."""
from aiogram.fsm.state import State, StatesGroup


class ServiceDateState(StatesGroup):
    """Класс ServiceDateState. Хранит информацию и данные вводимые пользователем."""

    service_date = State()
    service_time = State()
    service_cancel = State()
    service_delete = State()
    service_delete_conf = State()
    search_client = State()
    reserve_day = State()
    mailing_for_day = State()
