from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command='list',
            description='список напоминаний'
        ),
        BotCommand(
            command='setup',
            description='настройки'
        ),
        BotCommand(
            command='help',
            description='помощь'
        ),
        BotCommand(
            command='start',
            description='добавить напоминание'
        ),
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())