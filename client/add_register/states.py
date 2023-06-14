from aiogram.dispatcher.filters.state import State, StatesGroup


class AddRegisterState(StatesGroup):
    add_contact_name = State()
    add_contact_number = State()
