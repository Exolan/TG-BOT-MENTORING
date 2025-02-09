from aiogram.fsm.state import StatesGroup, State

class MenuState(StatesGroup):
    select_category = State()
    select_theme = State()