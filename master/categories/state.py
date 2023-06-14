from aiogram.dispatcher.filters.state import State, StatesGroup


class CategoriesState(StatesGroup):
    add_category = State()
    change_name = State()
