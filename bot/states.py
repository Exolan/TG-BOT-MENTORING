from aiogram.fsm.state import StatesGroup, State

class MenuState(StatesGroup):
    select_category = State()
    search_query = State()
    select_theme = State()