from aiogram.dispatcher.filters.state import State, StatesGroup


class AccountState(StatesGroup):
    add_master = State()
    change_name = State()
    change_contact = State()
