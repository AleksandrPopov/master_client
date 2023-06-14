from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from bots import bot_master
from master.categories.state import CategoriesState
from master.categories.callbacks import CategoriesCallback
from master.categories import categories_query, categories_message
from master import parse


async def categories_command(message: types.Message, state: FSMContext):
    await state.finish()
    await bot_master.del_messages(message=message)
    await categories_message.categories(message=message)


async def categories_message_handler(message: types.Message, state: FSMContext):
    await parse.state_cleaner(message=message, state=state)
    state_name = await state.get_state()

    if CategoriesState.add_category.state == state_name:
        await categories_message.add_category(message=message, state=state)

    if CategoriesState.change_name.state == state_name:
        await categories_message.change_name(message=message, state=state)


async def categories_query_handler(query: types.CallbackQuery, state: FSMContext):
    await parse.state_cleaner(message=query.message, state=state)

    if CategoriesCallback.ADD == query.data:
        await categories_query.add_category(query=query)

    if query.data.endswith(CategoriesCallback.MENU):
        await categories_query.menu_category(query=query, state=state)

    if CategoriesCallback.BACK == query.data:
        await categories_query.back_to_categories(query=query, state=state)

    if CategoriesCallback.CHANGE == query.data:
        await categories_query.change_name_category(query=query, state=state)

    if CategoriesCallback.DELETE == query.data:
        await categories_query.question_delete_category(query=query, state=state)

    if CategoriesCallback.DELETE_OK == query.data:
        await categories_query.delete_category(query=query, state=state)

    if CategoriesCallback.DELETE_CANCEL == query.data:
        await categories_query.back_menu_category(query=query, state=state)


async def register_categories_handlers(dp: Dispatcher):
    dp.register_message_handler(categories_command, commands=[CategoriesCallback.CATEGORIES])
    dp.register_message_handler(categories_message_handler, state=CategoriesState.all_states)
    dp.register_callback_query_handler(categories_query_handler,
                                       Text(endswith=CategoriesCallback.CATEGORIES_CALLBACK))
