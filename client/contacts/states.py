from aiogram.dispatcher.filters.state import State, StatesGroup


class ContactsState(StatesGroup):
    change_name = State()
    change_contact = State()
