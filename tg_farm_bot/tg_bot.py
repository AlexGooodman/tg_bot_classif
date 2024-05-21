import os
import asyncio
import logging
from dotenv import load_dotenv, find_dotenv
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters.command import Command
from core.utils.autoresetmiddlewares import AutoResetFSMMiddleware
from core.utils.antispammiddlwares import AntiSpamMiddleware
from core.keyboards.inline import show_admin_panel
from core.utils.statesform import Users_steps, Input_text
from core.utils.commands import set_commands
from core.handlers.admin_tools import show_users, get_all_users, give_text_from_message, cancel_input_for_message
from core.handlers.admin_tools import send_message_all_users, send_message_user, give_text_for_user
from core.handlers.basic import handle_start, button_handler, help_list, return_to_lobby
from core.handlers.steps_use import save_user_classif, callback_inline, save_line_from_dict
from core.handlers.steps_use import give_value_from_favourites, delete_line_from_favourites
from core.handlers.steps_use import choice_title_from_bd, add_classif

load_dotenv(find_dotenv())
TOKEN = os.environ.get('TOKEN', None)
ADMIN_ID = os.environ.get('ADMIN_ID', None)

async def start_bot_for_admin(bot: Bot):
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - [%(levelname)s] - %(name)s - "
                               "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")
    await set_commands(bot)
    await bot.send_message(ADMIN_ID, text='Бот запущен')

async def admin_tools(message: Message):
    if message.from_user.id == int(ADMIN_ID):
        await message.answer(f'🛠 Добро пожаловать в админ-панель, {message.from_user.first_name}',
                             reply_markup=show_admin_panel)
    else:
        await message.answer('Нет доступа!')

async def close_bot_for_admin(bot: Bot):
    await bot.send_message(ADMIN_ID, text='Бот остановлен')

async def start(message: Message):
    await handle_start(message)

async def main():
    bot = Bot(token=TOKEN)

    dp = Dispatcher()
    
    dp.startup.register(start_bot_for_admin)
    dp.shutdown.register(close_bot_for_admin)
    dp.message.middleware(AntiSpamMiddleware())
    dp.message.middleware(AutoResetFSMMiddleware())
    dp.callback_query.register(callback_inline, F.data=='show_value')
    dp.callback_query.register(save_line_from_dict, F.data=='saved_text')
    dp.callback_query.register(give_value_from_favourites, F.data=='show_value_favourites')
    dp.callback_query.register(delete_line_from_favourites, F.data=='delete_line')
    dp.callback_query.register(show_users, F.data=='show_users')
    dp.callback_query.register(get_all_users, F.data=='show_list_all_users')
    dp.callback_query.register(give_text_from_message, F.data=='say_all_users')
    dp.callback_query.register(give_text_for_user, F.data=='say_user')
    dp.callback_query.register(cancel_input_for_message, F.data=='cancel')
    dp.message.register(send_message_all_users, Input_text.text)
    dp.message.register(send_message_user, Input_text.text_from_user)
    dp.message.register(choice_title_from_bd, Users_steps.choice)
    dp.message.register(add_classif, Users_steps.add_choice)
    dp.message.register(start, Command('start'))
    dp.message.register(help_list, Command('help'))
    dp.message.register(return_to_lobby, Command('lobby'))
    dp.message.register(admin_tools, Command('admin'))
    dp.message.register(save_user_classif, F.document)
    dp.message.register(button_handler)


    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close

if __name__ == "__main__":
    asyncio.run(main())