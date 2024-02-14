"""Модуль запроса номера телефона пользователя"""
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


async def contact_button() -> ReplyKeyboardMarkup:
    """
    Функция создания клавиатуры contact_button.
    Воздаёт кнопки отправить телефон и вернуться.
    :return: ReplyKeyboardMarkup
    """
    keyboard_builder = ReplyKeyboardBuilder()
    keyboard_builder.button(text="📱 Отправить", request_contact=True)
    keyboard_builder.button(text="Вернуться")

    return keyboard_builder.as_markup(resize_keyboard=True)
