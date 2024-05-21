import time
from aiogram import Bot
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram import exceptions
from core.keyboards.inline import show_inline_cansel
from core.utils.statesform import Input_text
from database.db import get_len_users, get_users_id, get_all_users_for_txt


async def show_users(call: CallbackQuery):
    """Показывает сколько всего юзеров(счет из бд)"""
    await call.message.answer(f'Всего юзеров: 🧑‍💻<b>{get_len_users()}</b>',
                              parse_mode='HTML')
    await call.answer()

async def get_all_users(call: CallbackQuery, bot: Bot):
    """Отправляет txt документ со списком всех юзеров"""
    get_all_users_for_txt()
    chat_id = call.message.chat.id
    document = FSInputFile('files/users.txt')
    await bot.send_document(chat_id, document)
    await call.answer()

async def give_text_from_message(call: CallbackQuery, state: FSMContext):
    """Требует текст для отправки всем юзерам(прокладка)"""
    await call.message.answer('Введите текст, который хотите отправить всем юзерам!',
                              reply_markup=show_inline_cansel)
    await call.answer()
    await state.set_state(Input_text.text)


async def give_text_for_user(call: CallbackQuery, state: FSMContext):
    """Требует текст для отправки одному юзеру(прокладка)"""
    await call.message.answer('Введите user_id кому хотите отправить и текст сообщения через пробел!',
                              reply_markup=show_inline_cansel)
    await call.answer()
    await state.set_state(Input_text.text_from_user)


async def send_message_all_users(message: Message, state: FSMContext, bot: Bot):
    """Отправляет сообщение всем юзерам"""
    await state.update_data(text=message.text)
    data = await state.get_data()
    users = get_users_id()
    receive_users = 0
    block_users = 0
    for user in users:
        try:
            await bot.send_message(chat_id=user ,text=data['text'])
            receive_users += 1
            time.sleep(0.4)
        except exceptions.TelegramForbiddenError:
            block_users += 1
        except exceptions.TelegramRetryAfter:
            time.sleep(10)
    await message.answer(f'✅ Отправлено юзерам: <b>{receive_users}</b>\n⚠️ Заблокировали бота: <b>{block_users}</b>',
                         parse_mode='HTML')
    await state.clear()


async def send_message_user(message: Message, state: FSMContext, bot: Bot):
    """Отправляет сообщение одному юзеру"""
    mess = (message.text).split(' ')
    try:
        await bot.send_message(chat_id=mess[0], text=(' ').join(mess[1:]))
        await message.answer('Сообщение отправлено')
    except exceptions.TelegramForbiddenError:
        await message.answer('Не отправлено(заблокировал бота)')
    await state.clear()


async def cancel_input_for_message(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('ВЫ отменили действие')