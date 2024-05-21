from aiogram.fsm.state import StatesGroup, State

class Users_steps(StatesGroup):
    user_classif = State()
    user_count = State()
    user_saved_text = State()
    user_count_for_saved_text = State()
    choice = State()
    add_choice = State()

class Input_text(StatesGroup):
    text = State()
    text_from_user = State()

class ResetState(StatesGroup):
    last_activity = State()