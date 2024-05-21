import time
from aiogram import types
from aiogram.fsm.context import FSMContext
from core.keyboards.reply import reply_keyboards, reply_keyboard_actions
from database.db import save_user_in_bd
from core.handlers.steps_use import show_all_titles_from_bd, add_classif_message
from core.handlers.steps_use import give_next_key_from_classif, give_key_from_classif
from core.handlers.steps_use import start_user_classif_again, give_next_key_from_favourites
from core.handlers.steps_use import start_favourites_again
from core.handlers.steps_use import show_keyboard_for_favourites, delete_all_from_favorites
from core.utils.send_documents import send_documents

faq_info = '''
<b>Бот создан для помощи в изучении классификаций</b>
(создавался для фармакологических классификаций, но может работать с любыми другими классификациями)

<strong>Что умеет этот бот:</strong>
<b>1.</b> Выдает желаемые классификации в виде txt файла для изучения их.
<b>2.</b> Проводит, своего рода, тестирование пройденной классификации (заменяет те самые "карточки" в которых на одной стороне написан препарат, с другой стороны его группа).
<b>3.</b> "Тестирование" происходит в рандомном порядке, что позволяет создать симуляцию вашего ответа на паре.
<b>4.</b> В случае возникновения трудностей с запоминанием отдельных препаратов позволяет добавить их в избранное и провести <b>"Работу над ошибками"</b>
<b>5.</b> Позволяет загружать свои классификации для работы с ними(инструкции загрузки будут написаны ниже)

<strong>Инструкции для загрузки своей классификации</strong>
<b>1.</b> Бот принимает текстовый файл с расширением <u>.txt</u>.
<b>2.</b> Текст в файле должен быть форматирован с использованием таких условий: 
<i>- В конце каждых групп, подгрупп должно <b>ОБЯЗАТЕЛЬНО</b> стоять двоеточие!</i>
<i>- Каждый уровень подгруппы должен обозначаться табуляцией( или 4 пробела)!</i>
<i>- Пример форматирование вы можете посмотреть получив документ для изучения из имеющихся</i>
<i><b>- ЕСЛИ УСЛОВИЯ НЕ СОБЛЮДАЮТСЯ ВЫ ПОЛУЧИТЕ ОШИБКУ, ЕСЛИ СОБЛЮДАЮТСЯ ЧАСТИЧНО - КЛАССИФИКАЦИЯ БУДЕТ НЕПОЛНОЙ.</b></i> 

<strong>Правила использования Бота</strong>
<b>1.</b> Флуд запрещен, иначе получите блок на некоторое время.
<b>2.</b> Автосброс выбранных классификаций при неактивности через 1 час.
<b>3.</b> Если вдруг исчезли все кнопки - введите команду /lobby
<b>4.</b> Если потеряли это сообщение - введите команду /help
<b>5.</b> Вопросы и предложения по улучшению функционала бота, а также по поводу возникших багов - писать в телеграмм @imlittleprince 

<b>ПРИЯТНОГО ИСПОЛЬЗОВАНИЯ!!!</b>
'''

async def handle_start(message: types.Message):
    """ Обработка команды "start """
    save_user_in_bd(message.from_user.id, message.from_user.full_name)
    await message.answer(f"Привет, {message.from_user.first_name}")
    time.sleep(1)
    await return_to_lobby(message)

async def help_list(message: types.Message):
    """ Отправляет FAQ """
    await message.answer(faq_info, parse_mode='HTML')

async def return_to_lobby(message: types.Message):
    """ Возвращает в лобби """
    await message.answer('<b>Вы сейчас находитесь в лобби</b>',
                         parse_mode='html',
                         reply_markup=reply_keyboards)

async def show_faq_for_user(message: types.Message):
    """Отправляет FAQ"""
    await message.answer(faq_info,
                         parse_mode='html')

async def accept_document(message: types.Message):
    """ Текст с просьбой скинуть классификацю """
    markup_del = types.ReplyKeyboardRemove()
    await message.answer("Пришли мне свою классификацию.",
                         reply_markup=markup_del)

async def button_handler(message: types.Message, state: FSMContext):
    """Обработчик кнопок по присылаемому тексту"""
    if message.text == '📚Выбрать классификацию из списка📚':
        await show_all_titles_from_bd(message, state)
    elif message.text == '📌Добавить еще':
        await add_classif_message(message, state)
    elif message.text == '📩Получить документ(ы) для изучения📩':
        await send_documents(message, state)
    elif message.text == '📥Загрузить свою классификацию📥':
        await accept_document(message)
    elif message.text == '🔰F.A.Q':
        await show_faq_for_user(message)
    elif message.text == 'Начать✅' or message.text == 'Начать ✅':
        if message.text == 'Начать ✅':
            await message.answer('<b>Вот ваша классификация:</b>',
                                 parse_mode='HTML',
                                 reply_markup=reply_keyboard_actions)
        else:
            await message.answer('<b>Вот ваша классификация:</b>',
                                 parse_mode='HTML',
                                 reply_markup=reply_keyboard_actions)
        await give_key_from_classif(message, state)
    elif message.text == '🗒Далее':
        await give_next_key_from_classif(message, state)
    elif message.text == '♻️Заново':
        await start_user_classif_again(message, state)
    elif message.text == '📥Загрузить новую классификацию':
        await accept_document(message)
    elif message.text == '🕹В лобби':
        await return_to_lobby(message)
    elif message.text == '🧰Работа по избранному' or message.text =='🧰Избранное':
        await show_keyboard_for_favourites(message, state)
    elif message.text == '🗒 Далее':
        await give_next_key_from_favourites(message, state)
    elif message.text == '♻️ Заново':
        await start_favourites_again(message, state)
    elif message.text == '🗑 Очистить':
        await delete_all_from_favorites(message)  
