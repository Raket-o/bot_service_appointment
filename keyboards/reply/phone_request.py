"""Модуль запроса номера телефона пользователя."""
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


async def contact_button() -> ReplyKeyboardMarkup:
    """
    Функция создания клавиатуры contact_button.
    Воздаёт кнопки отправить телефон и вернуться.
    :return: ReplyKeyboardMarkup
    """
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton(text=("📱 Отправить"), request_contact=True))
    keyboard.add(KeyboardButton(text="Вернуться"))
    return keyboard
