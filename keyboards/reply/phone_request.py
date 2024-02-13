"""Модуль запроса номера телефона пользователя."""
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


async def contact_button() -> ReplyKeyboardMarkup:
    """
    Функция создания клавиатуры contact_button.
    Воздаёт кнопки отправить телефон и вернуться.
    :return: ReplyKeyboardMarkup
    """
    # keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    # keyboard.add(KeyboardButton(text=("📱 Отправить"), request_contact=True))
    # keyboard.add(KeyboardButton(text="Вернуться"))

    # keyboard = ReplyKeyboardMarkup(
    #     keyboard=[
    #         [
    #             KeyboardButton(text=("📱 Отправить"), request_contact=True),
    #             KeyboardButton(text="Вернуться")
    #         ],
    #     ],
    #     resize_keyboard=True
    # )

    keyboard_builder = ReplyKeyboardBuilder()
    keyboard_builder.button(text="📱 Отправить", request_contact=True)
    keyboard_builder.button(text="Вернуться")

    # return keyboard_builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
    return keyboard_builder.as_markup(resize_keyboard=True)
