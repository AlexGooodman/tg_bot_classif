from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault

async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command='start',
            description='Начать'
        ),
        BotCommand(
            command='lobby',
            description='Вернуться в лобби'
        ),
        BotCommand(
            command='help',
            description='Помощь'
        ),
        BotCommand(
            command='admin',
            description='админ-панель'
        )
    ]
    
    await bot.set_my_commands(commands, BotCommandScopeDefault())