from aiogram import types
from aiogram.dispatcher import FSMContext

import bots
from client.add_register import add_register_handlers
from client.add_register.callbacks import AddRegisterCallback
from client.contacts.callbacks import ContactsCallback
from client.contacts.contacts_handlers import contacts_command
from client.registers.callbacks import RegistersCallback
from client.registers.registers_handlers import registers_command


async def state_cleaner(message: types.Message, state: FSMContext):
    if message.text[1:] == AddRegisterCallback.START:
        await state.finish()
        await bots.bot_client.del_messages(message=message)
        await add_register_handlers.add_register_command(message=message, state=state)

    if message.text[1:] == RegistersCallback.REGISTERS:
        await state.finish()
        await bots.bot_client.del_messages(message=message)
        await registers_command(message=message, state=state)

    if message.text[1:] == ContactsCallback.CONTACTS:
        await state.finish()
        await bots.bot_client.del_messages(message=message)
        await contacts_command(message=message, state=state)
