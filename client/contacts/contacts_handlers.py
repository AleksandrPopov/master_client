from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

import bots
from client.contacts import contacts_query, contacts_messages
from client.contacts.callbacks import ContactsCallback
from client.contacts.states import ContactsState
from client import state_cleaner


async def contacts_command(message: types.Message, state: FSMContext):
    await state.finish()
    await bots.bot_client.del_messages(message=message)
    await contacts_messages.contacts(message=message)


async def contacts_message_handler(message: types.Message, state: FSMContext):
    await state_cleaner.state_cleaner(message=message, state=state)
    state_name = await state.get_state()

    if ContactsState.change_name.state == state_name:
        await contacts_messages.change_name(message=message, state=state)

    if ContactsState.change_contact.state == state_name:
        await contacts_messages.change_contact(message=message, state=state)


async def contact_query_handler(query: types.CallbackQuery, state: FSMContext):
    await state_cleaner.state_cleaner(message=query.message, state=state)

    if query.data.endswith(ContactsCallback.ID):
        await contacts_query.select_contact(query=query, state=state)

    if query.data.endswith(ContactsCallback.CHANGE_NAME):
        await contacts_query.change_name(query=query)

    if query.data.endswith(ContactsCallback.CHANGE_CONTACT):
        await contacts_query.change_contact(query=query)

    if query.data.endswith(ContactsCallback.DELETE):
        await contacts_query.delete_contact(query=query)

    if query.data.endswith(ContactsCallback.BACK_TO_CONTACTS):
        await contacts_query.back_to_contacts(query=query, state=state)

    if query.data.endswith(ContactsCallback.DELETE_CONFIRM):
        await contacts_query.delete_confirm(query=query, state=state)

    if query.data.endswith(ContactsCallback.CANCEL):
        await contacts_query.cancel_delete_contact(query=query, state=state)


async def register_contacts_handlers(dp: Dispatcher):
    dp.register_message_handler(contacts_command, commands=[ContactsCallback.CONTACTS])
    dp.register_message_handler(contacts_message_handler, state=ContactsState.all_states)
    dp.register_callback_query_handler(contact_query_handler, Text(endswith=ContactsCallback.CONTACTS))
