from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

import bots
from client.registers import registers_query
from client.registers import registers_messages
from client.registers.callbacks import RegistersCallback


async def registers_command(message: types.Message, state: FSMContext):
    await state.finish()
    await bots.bot_client.del_messages(message=message)
    await registers_messages.registers(message=message, state=state)


async def registers_query_handler(query: types.CallbackQuery, state: FSMContext):
    if query.data.endswith(RegistersCallback.DELETE):
        await registers_query.delete_registers(query=query, state=state)

    if query.data.endswith(RegistersCallback.DELETE_CONFIRM):
        await registers_query.delete_confirm(query=query, state=state)

    if query.data.endswith(RegistersCallback.CANCEL):
        await registers_query.delete_cancel(query=query, state=state)


async def register_registers_handlers(dp: Dispatcher):
    dp.register_message_handler(registers_command, commands=[RegistersCallback.REGISTERS])
    dp.register_callback_query_handler(registers_query_handler, Text(endswith=RegistersCallback.REGISTERS))