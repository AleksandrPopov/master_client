from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ContentType

from bots import bot_master
from master.account.account_message import start
from master.account.state import AccountState
from master.account.callbacks import AccountCallback, StartCommand
from master.account import account_query, account_message
from master import parse


async def account_command(message: types.Message, state: FSMContext):
    await state.finish()
    await bot_master.del_messages(message=message)

    if message.text[1:] == StartCommand.START:
        await start(message=message)

    if message.text[1:] == AccountCallback.ACCOUNT:
        await account_message.account(message=message)


async def account_message_handler(message: types.Message, state: FSMContext):
    await parse.state_cleaner(message=message, state=state)
    state_name = await state.get_state()

    if AccountState.change_name.state == state_name:
        await account_message.change_name(message=message, state=state)

    if AccountState.change_contact.state == state_name:
        await account_message.change_contact(message=message, state=state)


async def account_query_handler(query: types.CallbackQuery, state: FSMContext):
    await parse.state_cleaner(message=query.message, state=state)

    if AccountCallback.CHANGE_NAME == query.data:
        await account_query.change_name(query=query)

    if AccountCallback.CHANGE_CONTACT == query.data:
        await account_query.change_contact(query=query)

    if AccountCallback.DELETE_ACCOUNT == query.data:
        await account_query.delete(query=query)

    if AccountCallback.DELETE_CANCEL == query.data:
        await account_query.cancel(query=query)

    if AccountCallback.DELETE_CONFIRM == query.data:
        await account_query.delete_confirm(query=query, state=state)


async def contact_handler(message: types.Message):
    await bot_master.del_messages(message=message)
    await account_message.add_master(message=message)


async def register_account_handlers(dp: Dispatcher):
    dp.register_message_handler(account_command, commands=[StartCommand.START, AccountCallback.ACCOUNT])
    dp.register_message_handler(account_message_handler, state=AccountState.all_states)
    dp.register_message_handler(contact_handler, content_types=ContentType.CONTACT)
    dp.register_callback_query_handler(account_query_handler, Text(startswith=AccountCallback.ACCOUNT))
