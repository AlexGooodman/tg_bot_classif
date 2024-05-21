from aiogram.types import Message, FSInputFile
from aiogram.types import InputMediaDocument
from aiogram.fsm.context import FSMContext


async def send_documents(message: Message, state: FSMContext):
    """Отправляет txt документы с классификациями"""
    data = await state.get_data()
    try:
        files_to_send = data['choice']
        media_group = list()
        for f in files_to_send:
            media_group.append(InputMediaDocument(media=FSInputFile(f)))
        await message.answer_media_group(media=media_group)
    except KeyError:
        await message.answer('<b>Не актуально. Отсутствует классификация 😐</b>',
                             parse_mode='HTML')