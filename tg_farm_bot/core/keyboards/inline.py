from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

show_value_for_key = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='👁',
            callback_data='show_value'
        ),
        InlineKeyboardButton(
            text='⭐️',
            callback_data='saved_text'
        )
    ]
])

show_value_for_key_in_favourites = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='👁',
            callback_data='show_value_favourites'
        ),
        InlineKeyboardButton(
            text='❌',
            callback_data='delete_line'
        )
    ]
])

show_admin_panel = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='Всего юзеров 🧑‍💻',
            callback_data='show_users'
        ),
        InlineKeyboardButton(
            text='Cписок юзеров ⚙️',
            callback_data='show_list_all_users'
        )
    ],
    [
        InlineKeyboardButton(
            text='Сообщение всем 📢',
            callback_data='say_all_users'
        ),
        InlineKeyboardButton(
            text='Сообщение одному 💬',
            callback_data='say_user'
        )
    ],
])

show_inline_cansel = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text = 'Отмена',
            callback_data='cancel'
        )
    ]
])