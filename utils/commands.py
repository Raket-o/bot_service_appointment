"""Модуль команд для бота"""
from aiogram import Bot, types


async def set_default_commands(bot: Bot):
    commands = [
        types.BotCommand(command="start", description="Запустить бота"),
    ]
    await bot.set_my_commands(commands=commands)
