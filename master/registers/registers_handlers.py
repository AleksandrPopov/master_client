from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from bots import bot_master
from master.registers import registers_query
from master.registers import registers_message
from master.registers.callbacks import RegistersCallback
from master import parse


async def registers_command(message: types.Message, state: FSMContext):
    await state.finish()
    await bot_master.del_messages(message=message)
    await registers_message.registers(message=message)


async def registers_query_handler(query: types.CallbackQuery, state: FSMContext):
    await parse.state_cleaner(message=query.message, state=state)

    if query.data.endswith(RegistersCallback.REGISTER):
        await registers_query.register(query=query, state=state)

    if query.data.endswith(RegistersCallback.DELETE):
        await registers_query.delete(query=query)

    if query.data.endswith(RegistersCallback.DELETE_CONFIRM):
        await registers_query.delete_confirm(query=query, state=state)

    if query.data.endswith(RegistersCallback.CANCEL):
        await registers_query.cancel(query=query)

    if query.data.endswith(RegistersCallback.BACK_TO_DATE):
        await registers_query.back_to_date(query=query, state=state)

    if query.data.endswith(RegistersCallback.BACK_TO_TIME):
        await registers_query.back_to_time(query=query, state=state)

    if query.data.endswith(RegistersCallback.IGNORE):
        await query.answer(cache_time=60)


async def registers_select(query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await registers_query.date_selector(query=query, data=callback_data, state=state)


async def register_registers_handlers(dp: Dispatcher):
    dp.register_message_handler(registers_command, commands=[RegistersCallback.REGISTERS])
    dp.register_callback_query_handler(registers_query_handler, Text(endswith=RegistersCallback.REGISTERS))
    dp.register_callback_query_handler(registers_select, RegistersCallback.REGISTERS_CALLBACK.filter())
