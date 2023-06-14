from aiogram.dispatcher.filters.state import State, StatesGroup


class ServicesState(StatesGroup):
    add_name = State()
    add_time = State()
    add_cost = State()
    add_service = State()
    change_name = State()
    change_time = State()
    change_cost = State()
