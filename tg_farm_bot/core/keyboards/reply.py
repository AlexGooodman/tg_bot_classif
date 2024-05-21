from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

reply_keyboards = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text='📚Выбрать классификацию из списка📚',
        ),
    ],
    [
        KeyboardButton(
            text='📥Загрузить свою классификацию📥',
        )
    ],
    [
        KeyboardButton(
            text='🧰Избранное',
        ),
        KeyboardButton(
            text='🔰F.A.Q',
        )
    ]
], resize_keyboard=True, one_time_keyboard=True)

reply_keyboard_start = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text='Начать ✅',
        ),
    ]
], resize_keyboard=True, one_time_keyboard=True)

reply_keyboard_actions = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text='🗒Далее',
        ),
        KeyboardButton(
            text='♻️Заново',
        )
    ],
    [
        KeyboardButton(
            text='🕹В лобби',
        )
    ]
], resize_keyboard=True)

reply_keyboard_actions_for_favourites = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text='🗒 Далее',
        ),
    ],
    [
        KeyboardButton(
            text='♻️ Заново',
        ),
        KeyboardButton(
            text='🗑 Очистить',
        ),
    ],
    [
        KeyboardButton(
            text='🕹В лобби',
        ),
    ],
], resize_keyboard=True)

reply_keyboards_choice = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text='Начать✅',
        ),
        KeyboardButton(
            text='📌Добавить еще',
        )
    ],
    [
        KeyboardButton(
            text='📩Получить документ(ы) для изучения📩',
        )
    ]
], resize_keyboard=True)
