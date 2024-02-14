"""Модуль генерации клавиатуры. Имя берётся из входящего списка"""
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def list_button(tpl: tuple) -> ReplyKeyboardMarkup:
    """
    Функция создания клавиатуры list_button.
    Принимает на вход список где lst[1]: str - названия кнопок,
    (если значение lst[1]= -1, пропускает)
    остальные элементы опциональны.
    :return: ReplyKeyboardMarkup
    """
    keyboard_builder = ReplyKeyboardBuilder()
    btns = ([KeyboardButton(text=i_lst[1]) for i_lst in tpl if i_lst[1] != -1])
    keyboard_builder.add(*btns)
    keyboard_builder.adjust(2)

    return keyboard_builder.as_markup(resize_keyboard=True)
