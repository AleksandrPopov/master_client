from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ContentType

import bots
from client.add_register import add_register_query, add_register_message
from client.add_register.callbacks import AddRegisterCallback
from client.add_register.states import AddRegisterState
from client import state_cleaner


async def add_register_command(message: types.Message, state: FSMContext):
    await state.finish()
    await bots.bot_client.del_messages(message=message)
    await add_register_message.start(message=message, state=state)


async def add_register_message_handler(message: types.Message, state: FSMContext):
    await state_cleaner.state_cleaner(message=message, state=state)
    state_name = await state.get_state()

    if AddRegisterState.add_contact_name.state == state_name:
        await add_register_message.add_contact_name(message=message, state=state)

    if AddRegisterState.add_contact_number.state == state_name:
        await add_register_message.add_contact_number(message=message, state=state)


async def add_register_query_handler(query: types.CallbackQuery, state: FSMContext):
    if query.data.endswith(AddRegisterCallback.CATEGORY):
        await add_register_query.categories(query=query, state=state)

    if query.data.endswith(AddRegisterCallback.SERVICE):
        await add_register_query.services(query=query, state=state)

    if query.data.endswith(AddRegisterCallback.MORE):
        await add_register_query.more_services(query=query, state=state)

    if query.data.endswith(AddRegisterCallback.PRICE):
        await add_register_query.price(query=query, state=state)

    if query.data.endswith(AddRegisterCallback.DATE):
        await add_register_query.date(query=query, state=state)

    if query.data.endswith(AddRegisterCallback.TIME):
        await add_register_query.time(query=query, state=state)

    if query.data.endswith(AddRegisterCallback.CONTACT):
        await add_register_query.contact(query=query, state=state)

    if query.data.endswith(AddRegisterCallback.ADD_CONTACT):
        await add_register_query.add_contact(query=query, state=state)

    if query.data.endswith(AddRegisterCallback.CONFIRM_REGISTER):
        await add_register_query.confirm_register(query=query, state=state)

    if query.data.endswith(AddRegisterCallback.ADD_TO_DB):
        await add_register_query.add_register_to_db(query=query, state=state)

    if query.data.endswith(AddRegisterCallback.OK):
        pass

    # Back buttons.
    if query.data.endswith(AddRegisterCallback.BACK_TO_MASTERS):
        await add_register_query.back_to_masters(query=query, state=state)

    if query.data.endswith(AddRegisterCallback.BACK_TO_CATEGORY):
        await add_register_query.back_to_categories(query=query, state=state)

    if query.data.endswith(AddRegisterCallback.BACK_TO_SERVICE):
        await add_register_query.back_to_services(query=query, state=state)

    if query.data.endswith(AddRegisterCallback.BACK_TO_MORE):
        await add_register_query.back_to_more_services(query=query, state=state)

    if query.data.endswith(AddRegisterCallback.BACK_TO_DATE):
        await add_register_query.back_to_date(query=query, state=state)

    if query.data.endswith(AddRegisterCallback.BACK_TO_TIME):
        await add_register_query.back_to_time(query=query, state=state)

    if query.data.endswith(AddRegisterCallback.BACK_TO_CONTACT):
        await add_register_query.back_to_contact(query=query, state=state)


async def date_select(query: types.CallbackQuery, state: FSMContext, callback_data: dict):
    await add_register_query.date_selector(query=query, state=state, data=callback_data)


async def get_contact(message: types.Message, state: FSMContext):
    await bots.bot_client.del_messages(message=message)
    await add_register_message.add_contact(message=message, state=state)


async def register_add_register_handlers(dp: Dispatcher):
    dp.register_message_handler(add_register_command, commands=[AddRegisterCallback.START])
    dp.register_message_handler(add_register_message_handler, state=AddRegisterState.all_states)
    dp.register_message_handler(get_contact, content_types=ContentType.CONTACT)
    dp.register_callback_query_handler(add_register_query_handler, Text(endswith=AddRegisterCallback.ADD_REGISTER))
    dp.register_callback_query_handler(date_select, AddRegisterCallback.DATE_CALLBACK.filter())
