from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from bots import bot_master
from master.services.state import ServicesState
from master.services.callbacks import ServicesCallback
from master.services import services_message, services_query
from master import parse


async def services_command(message: types.Message, state: FSMContext):
    await state.finish()
    await bot_master.del_messages(message=message)
    await services_message.services(message=message)


async def services_message_handler(message: types.Message, state: FSMContext):
    await parse.state_cleaner(message=message, state=state)
    state_name = await state.get_state()

    if ServicesState.add_name.state == state_name:
        await services_message.add_time(message=message, state=state)

    if ServicesState.add_time.state == state_name:
        await services_message.add_cost(message=message, state=state)

    if ServicesState.add_cost.state == state_name:
        await services_message.add_service(message=message, state=state)

    if ServicesState.change_name.state == state_name:
        await services_message.change_name(message=message, state=state)

    if ServicesState.change_time.state == state_name:
        await services_message.change_time(message=message, state=state)

    if ServicesState.change_cost.state == state_name:
        await services_message.change_cost(message=message, state=state)


async def services_query_handler(query: types.CallbackQuery, state: FSMContext):
    await parse.state_cleaner(message=query.message, state=state)

    if ServicesCallback.ADD_NAME == query.data:
        await services_query.add_name(query=query, state=state)

    if ServicesCallback.BACK_CATEGORIES == query.data:
        await services_query.back_to_categories(query=query)

    if query.data.endswith(ServicesCallback.SERVICES_LIST):
        await services_query.services(query=query, state=state)

    if ServicesCallback.ADD_SERVICE == query.data:
        await services_query.add_service(query=query, state=state)

    if query.data.endswith(ServicesCallback.MENU):
        await services_query.menu(query=query, state=state)

    if ServicesCallback.CHANGE_NAME == query.data:
        await services_query.change_name(query=query, state=state)

    if ServicesCallback.CHANGE_TIME == query.data:
        await services_query.change_time(query=query, state=state)

    if ServicesCallback.CHANGE_COST == query.data:
        await services_query.change_cost(query=query, state=state)

    if ServicesCallback.BACK_SERVICES == query.data:
        await services_query.back_to_services(query=query, state=state)

    if ServicesCallback.DELETE == query.data:
        await services_query.delete_service(query=query, state=state)

    if ServicesCallback.DELETE_CANCEL == query.data:
        await services_query.delete_cancel(query=query, state=state)

    if ServicesCallback.DELETE_OK == query.data:
        await services_query.delete_ok(query=query, state=state)


async def register_services_handlers(dp: Dispatcher):
    dp.register_message_handler(services_command, commands=[ServicesCallback.SERVICES])
    dp.register_message_handler(services_message_handler, state=ServicesState.all_states)
    dp.register_callback_query_handler(services_query_handler, Text(endswith=ServicesCallback.SERVICES_CALLBACK))
