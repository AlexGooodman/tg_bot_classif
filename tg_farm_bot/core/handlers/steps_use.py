import re, os, string
from typing import Union
from aiogram import Bot
from aiogram.types import Message
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from database.db import get_all_titles_from_data, get_title_from_data, get_path_to_file
from database.db import save_line_for_user_favourites, delete_line_from_bd, delete_all_user_line_from_bd
from database.db import get_user_favourites_in_bd, show_choice_classif, get_path_to_many_files, get_path_to_many_random_files
from database.db import show_choice_random_classif
from core.utils.statesform import Users_steps
from core.keyboards.reply import reply_keyboard_start, reply_keyboards
from core.keyboards.reply import reply_keyboard_actions_for_favourites
from core.keyboards.reply import reply_keyboards_choice
from core.keyboards.inline import show_value_for_key, show_value_for_key_in_favourites
from core.parser_logic.finaly_dict import create_dict, randomize_keys


# *******************************************************************************************************************
# Общие функции
# *******************************************************************************************************************

def show_key_from_dict(dictionary: dict, counter: int) -> Union[str, bool]:
    """Функция принимает словарь и возвращет ключ"""
    if len(list(dictionary.keys())) > counter:
        keys_list = list(dictionary.keys())
        key = keys_list[counter]
        return key
    else:    
        return False


def show_value_from_dict(dictionary: dict, message_text: str) -> Union[str, bool]:
    """Функция принимает словарь и возвращет значение из ключа"""
    value = dictionary[f' {message_text}']
    return value


def couner_add(counter: int) -> int:
    """Повышает счетчик состояния пользователей для перехода на следующую строку словаря)"""
    counter += 1
    return counter

def couner_step_down(counter: int) -> int:
    """Повышает счетчик состояния пользователей для перехода на следующую строку словаря)"""
    counter -= 1
    return counter

def delete_from_dict(dictionary: dict, key: str) -> dict:
    """Удаляет линию из словаря"""
    dictionary.pop(key)
    return dictionary

def get_dict_classifications(file):
    """Парсит и перемешивает спаршенный словарь при загрузке пользователем классификации"""
    data_classif = create_dict(file)
    return data_classif

def get_dict_many_classif(file):
    """Парсит и перемешивает спаршенный словарь при загрузке пользователем нескольких классификаций"""
    with open("database/storage/result.txt", "w", encoding="utf-8") as outfile:
        for f in file:
            with open(f, "r", encoding="utf-8") as infile:
                outfile.write('\n')
                outfile.write(infile.read())
    data_classif = create_dict("database/storage/result.txt")
    os.remove("database/storage/result.txt")

    return data_classif

def join_many_dictionary(firs_dict: dict, second_dict: dict) -> dict:
    """Объединяет два словаря"""
    x = second_dict.copy()
    x.update(firs_dict)
    return x



# *******************************************************************************************************************
# Функции связанные с базой данных
# *******************************************************************************************************************

async def start_classif_from_bd(message: Message):
    """Прокладка для показа нового кейборда"""
    await message.reply('Готовы?',
                        reply_markup=reply_keyboards_choice)

async def add_classif_message(message: Message, state: FSMContext):
    """Инструкция для пользователя"""
    await message.answer('<b>Выберите нужную классификацию указав одну цифру или число</b>',
                         parse_mode='HTML')
    await state.set_state(Users_steps.add_choice)

async def add_classif(message: Message, state: FSMContext):
    """Подгружает выбранную классификацию"""
    if (message.text).isdigit() is False:
        await message.answer('Это не цифра и не число!')
    elif get_path_to_file(message.text) is False: 
        await message.answer('Такого нет в списке! Повторите еще раз 😤')
    else:
        await message.answer(f'Вы выбрали тему: <b>{get_title_from_data(message.text)}</b>',
                             parse_mode='HTML')
        await state.update_data(add_choice=get_path_to_file(message.text))
        data = await state.get_data()
        await state.set_state(Users_steps.user_classif)
        await upload_next_file_classif(data['add_choice'], state, message)


async def upload_next_file_classif(path_for_classif: str, state: FSMContext, message: Message):
    """Парсит выбранную классификацию и добавляет в предыдущую"""
    try:
        await start_classif_from_bd(message)
        await state.set_state(Users_steps.user_classif)
        data = await state.get_data()
        current_dict = data['user_classif']
        new_dict = get_dict_classifications(path_for_classif)
        await state.update_data(user_classif=randomize_keys(join_many_dictionary(current_dict, new_dict)))
        await state.set_state(Users_steps.user_count)
        await state.update_data(user_count=0)
    except KeyError:
        await message.answer('Ошибка! Возвращаю вас в лобби.',
                             reply_markup=reply_keyboards)
        

async def show_all_titles_from_bd(message: Message, state: FSMContext):
    """Предлагает выбор классификации из списка"""
    await message.answer(f'<b>Вот что у меня есть:</b>\n{get_all_titles_from_data()}',
                         parse_mode='HTML')
    await message.answer('<b>Выберите нужную классификацию указав цифру</b>\n(Пример: "1" или "1-5" или "1,2,3").',
                         parse_mode='HTML')
    await state.set_state(Users_steps.choice)


async def choice_title_from_bd(message: Message, state: FSMContext):
    """Проверяет выбор юзера на корректность и запускает классификацию функцией 'upload_file_classif'"""
    if re.match(r'\d+-\d+', message.text):
        numb1 = str(re.findall(r'\d+(?=-)', message.text)[0])
        numb2 = str(re.findall(r'(?<=-)\d+', message.text)[0])
        if get_path_to_many_files(numb1, numb2) is not False:
            await message.answer(f'Вы выбрали темы: <b>{show_choice_classif(numb1, numb2)}</b>',
                             parse_mode='HTML')
            await state.update_data(choice=get_path_to_many_files(numb1, numb2))
            data = await state.get_data()
            await state.set_state(Users_steps.user_classif)
            await upload_many_files_classif(data['choice'], state, message)
        else:
            await message.answer('Список пуст! Проверьте корректность выбранных тем и повторите еще раз. 😤')
    elif re.match(r'\d+(,\d+)*', message.text):
        numbs = (message.text).strip(string.punctuation)
        if get_path_to_many_random_files(numbs) is not False:
            await message.answer(f'Вы выбрали темы: <b>{show_choice_random_classif(numbs)}</b>',
                                 parse_mode='HTML')
            await state.update_data(choice=get_path_to_many_random_files(numbs))
            data = await state.get_data()
            await state.set_state(Users_steps.user_classif)
            await upload_many_files_classif(data['choice'], state, message)
        else:
            await message.answer('Список пуст! Проверьте корректность выбранных тем и повторите еще раз. 😤') 
    elif (message.text).isdigit() is False:
        if get_path_to_file(message.text) is False:
            await message.answer('Такого нет в списке! Повторите еще раз 😤')
        else:
            await message.answer('Это не цифра и даже не число!')
    else: 
        await message.answer(f'Вы выбрали тему: <b>{get_title_from_data(message.text)}</b>',
                             parse_mode='HTML')
        await state.update_data(choice=get_path_to_file(message.text))
        data = await state.get_data()
        await state.set_state(Users_steps.user_classif)
        await upload_file_classif(data['choice'], state, message)


async def upload_file_classif(path_for_classif: str, state: FSMContext, message: Message):
    """Парсит выбранную классификацию, дает старт её началу"""
    await start_classif_from_bd(message)
    await state.set_state(Users_steps.user_classif)
    await state.update_data(user_classif=get_dict_classifications(path_for_classif))
    await state.set_state(Users_steps.user_count)
    await state.update_data(user_count=0)

async def upload_many_files_classif(path_for_classif: list, state: FSMContext, message: Message):
    """Парсит выбранные классификации, дает старт её началу"""
    await start_classif_from_bd(message)
    await state.set_state(Users_steps.user_classif)
    await state.update_data(user_classif=get_dict_many_classif(path_for_classif))
    await state.set_state(Users_steps.user_count)
    await state.update_data(user_count=0)




# *******************************************************************************************************************
# Основные функции для пользовательского документа
# *******************************************************************************************************************

async def start_classifications(message: Message):
    """Выводит кнопку(промежуточное звено между функциями save_user_classif и give_key_from_classif)"""
    await message.reply('Готовы?',
                        reply_markup=reply_keyboard_start)


async def save_user_classif(message: Message,state: FSMContext, bot: Bot):
    """Сохраняет присланный документ и создает состояние юзеру"""
    # await state.clear()
    file = await bot.get_file(message.document.file_id)
    await bot.download_file(file.file_path, 'downloaded.txt')
    await start_classifications(message)
    await state.set_state(Users_steps.user_classif)
    await state.update_data(user_classif=get_dict_classifications('downloaded.txt'))
    await state.set_state(Users_steps.user_count)
    await state.update_data(user_count=0)

    

async def give_key_from_classif(message: Message, state: FSMContext):
    """Показывает первый ключ из словаря, выводит новый кейборд"""
    try:
        data = await state.get_data()
        if data['user_classif'] is False:
            await message.answer('<b>Неверный формат классификации. Проверьте наличие ":" или табуляций 🧐</b>',
                                parse_mode='HTML',
                                reply_markup=reply_keyboards)
        elif data['user_classif'] == None:
            await message.answer('<b>Классификация должна быть текстовым файлом(.txt) 😤</b>',
                                parse_mode='HTML',
                                reply_markup=reply_keyboards)
        else:
            if show_key_from_dict(data['user_classif'], data['user_count']) is False:
                await message.answer('<b>Достигнут конец классификации! ✅</b>',
                                    parse_mode='HTML')
            else:
                await message.answer('👁 - Показать группу препарата;\n⭐️ - добавить препарат в избранное')
                await message.answer(show_key_from_dict(data['user_classif'], data['user_count']),
                                    reply_markup=show_value_for_key)
                await state.set_state(Users_steps.user_classif)
    except KeyError:
        await message.answer('Тут пусто 🤷‍♂️',
                             reply_markup=reply_keyboards)

async def give_next_key_from_classif(message: Message, state: FSMContext):
    """
    Выводит последующие ключи из словаря. Обработка ошибки 
    KeyError при отсутствии классификации.
    """
    try:
        data = await state.get_data()
        await state.update_data(user_count=couner_add(data['user_count']))
        data = await state.get_data()
        if show_key_from_dict(data['user_classif'], data['user_count']) is False:
            await message.answer('<b>Достигнут конец классификации! ✅</b>',
                                 parse_mode='HTML')
        else:
            await message.answer(show_key_from_dict(data['user_classif'], data['user_count']),
                                reply_markup=show_value_for_key)
    except KeyError:
        await message.answer('<b>Сначала загрузите классификацию 😐</b>',
                             parse_mode='HTML')


async def start_user_classif_again(message: Message, state: FSMContext):
    """Начинает классификацию сначала, перетасовует, если её нет в базе - выводит ошибку"""
    try:
        data = await state.get_data()
        await state.update_data(user_classif=randomize_keys(data['user_classif']))
        await start_classifications(message)
        await state.set_state(Users_steps.user_count)
        await state.update_data(user_count=0)
    except KeyError:
        await message.answer('<b>Сначала загрузите классификацию 😐</b>',
                             parse_mode='HTML')


async def callback_inline(call: CallbackQuery, state: FSMContext):
    """Обработка инлайн кнопки 'Показать группу'"""
    try:
        data = await state.get_data()
        if len(show_value_from_dict(data['user_classif'], call.message.text)) > 200:
            await call.message.answer(show_value_from_dict(data['user_classif'], call.message.text),
                                    show_alert=True)
            await call.answer('Длина сообщения превышает лимиты в телеграмм.\nСкинул обычным сообщением ниже.')
        else:
            await call.answer(show_value_from_dict(data['user_classif'], call.message.text),
                                    show_alert=True)
    except KeyError:
        await call.message.answer('<b>Сначала загрузите классификацию 😐</b>',
                             parse_mode='HTML')
        await call.answer()


# *******************************************************************************************************************
# Функции для работы с избранными строчками
# *******************************************************************************************************************

async def show_keyboard_for_favourites(message: Message,state: FSMContext):
    """Прокладка для обновления клавиатуры"""
    await state.update_data(user_saved_text=get_user_favourites_in_bd(message.from_user.id))
    await state.set_state(Users_steps.user_count_for_saved_text)
    await state.update_data(user_count_for_saved_text=0)
    await work_from_favourites(message, state)


async def work_from_favourites(message: Message,state: FSMContext):
    """Выдает строчки из избранного"""
    try:
        data = await state.get_data()
        if data['user_saved_text'] is not None:
            await message.answer('<b>Вот ваше избранное:</b>',
                                 parse_mode='HTML',
                                 reply_markup=reply_keyboard_actions_for_favourites)
            await message.answer('👁 - Показать группу препарата;\n❌ - удалить препарат из избранного')
            await message.answer(show_key_from_dict(data['user_saved_text'], data['user_count_for_saved_text']),
                                                    reply_markup=show_value_for_key_in_favourites)
        else:
            await message.answer('Тут пусто 🤷‍♂️')
    except KeyError:
        await message.answer('Тут пусто 🤷‍♂️')


async def give_value_from_favourites(call: CallbackQuery, state: FSMContext):
    """Обработка инлайн кнопки 'Показать группу для избранного'"""
    try:
        data = await state.get_data()
        if data['user_saved_text'] != None:
            if len(show_value_from_dict(data['user_saved_text'], call.message.text)) > 200:
                await call.message.answer(show_value_from_dict(data['user_saved_text'], call.message.text))
                await call.answer('Длина сообщения превышает лимиты в телеграмм.\nСкинул обычным сообщением ниже.')
            else:
                await call.answer(show_value_from_dict(data['user_saved_text'], call.message.text),
                                        show_alert=True)
        else: 
            await call.answer('Не актуально 😐')
    except KeyError:
        await call.answer('Не актуально 😐')



async def give_next_key_from_favourites(message: Message, state: FSMContext):
    """
    Выводит последующие ключи из словаря. 
    """
    try:
        data = await state.get_data()
        await state.update_data(user_count_for_saved_text=couner_add(data['user_count_for_saved_text']))
        data = await state.get_data()
        if show_key_from_dict(data['user_saved_text'], data['user_count_for_saved_text']) is False:
            await message.answer('<b>Достигнут конец классификации! ✅</b>',
                                 parse_mode='HTML')
        else:
            await message.answer(show_key_from_dict(data['user_saved_text'], data['user_count_for_saved_text']),
                                                    reply_markup=show_value_for_key_in_favourites)
    except KeyError:
        await message.answer('<b>А что вам показывать, если тут пусто?</b>',
                             parse_mode='HTML')


async def start_favourites_again(message: Message, state: FSMContext):
    """Начинает классификацию сначала, перетасовует, если её нет в базе - выводит ошибку"""
    try:
        await state.update_data(user_saved_text=get_user_favourites_in_bd(message.from_user.id))
        if get_user_favourites_in_bd(message.from_user.id) is not None:
            await state.set_state(Users_steps.user_count_for_saved_text)
            await state.update_data(user_count_for_saved_text=0)
            data = await state.get_data()
            await state.update_data(user_saved_text=randomize_keys(data['user_saved_text']))
            await work_from_favourites(message, state)
        else:
            await message.answer('<b>Достигнут конец классификации! ✅</b>',
                                 parse_mode='HTML',
                                 reply_markup=reply_keyboards)
    except KeyError:
        await message.answer('<b>Тогда вам стоит вернуться в лобби и выбрать режим.</b>',
                             parse_mode='HTML')


# async def return_in_user_classif(message: Message, state: FSMContext):
#     """Возвращает к пользовательствкой классификации продолжая(не сбрасывает счетчик)"""
#     await message.answer('<b>Сделано! Продолжаю вашу классификацию</b>',
#                          parse_mode='HTML',
#                          reply_markup=reply_keyboard_actions)
#     await give_key_from_classif(message, state)


async def delete_line_from_favourites(call: CallbackQuery):
    """Удаляет строку из бд(favourites), при нажатии на инлайн кнопку"""
    try:
        key = f' {call.message.text}'
        delete_line_from_bd(call.from_user.id, key)
        await call.answer(f'Удалил: {key} ✅')
    except KeyError:
        await call.answer('Не актуально 😐')


async def delete_all_from_favorites(message: Message):
    """Очищает полностью избранное из бд"""
    await message.answer('<b>Теперь в избранном ничего нет 👍</b>',
                         parse_mode='HTML',
                         reply_markup=reply_keyboards)
    delete_all_user_line_from_bd(message.from_user.id)


async def save_line_from_dict(call: CallbackQuery, state: FSMContext):
    """Добавляет в таблицу бд(favourites) ключ и значение"""
    try:
        data = await state.get_data()
        key = f' {call.message.text}'
        value = show_value_from_dict(data['user_classif'], call.message.text)
        save_line_for_user_favourites(call.from_user.id, key, value)
        await call.answer(f'Добавлено: {key} ✅')
    except KeyError:
        await call.answer('Добавить невозможно(не актуально)')