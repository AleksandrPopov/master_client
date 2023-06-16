from contextlib import suppress

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentTypes
from aiogram.utils.exceptions import MessageToDeleteNotFound, MessageCantBeDeleted

from client.add_register.callbacks import AddRegisterCallback
from client.contacts.callbacks import ContactsCallback
from master.registers.callbacks import RegistersCallback


async def close(message: types.Message, state: FSMContext):
    commands_list = [
        AddRegisterCallback.START,
        RegistersCallback.REGISTERS,
        ContactsCallback.CONTACTS
    ]
    if await state.get_state() is None or message.text[1:] not in commands_list:
        with suppress(MessageToDeleteNotFound, MessageCantBeDeleted):
            await message.delete()


async def register_filter_handler(dp: Dispatcher):
    dp.register_message_handler(close, content_types=ContentTypes.ANY)
