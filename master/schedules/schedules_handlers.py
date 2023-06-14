from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from bots import bot_master
from master.schedules.callbacks import SchedulesCallback
from master.schedules import schedules_query, schedules_message


async def schedules_command(message: types.Message, state: FSMContext):
    await state.finish()
    await bot_master.del_messages(message=message)
    if message.text[1:] in SchedulesCallback.SCHEDULES:
        await schedules_message.schedules(message=message)


async def schedules_query_handler(query: types.CallbackQuery, callback_data: dict):
    await schedules_query.schedules_selector(query=query, data=callback_data)


async def register_schedules_handlers(dp: Dispatcher):
    dp.register_message_handler(schedules_command, commands=[SchedulesCallback.SCHEDULES])
    dp.register_callback_query_handler(schedules_query_handler, SchedulesCallback.SCHEDULES_CALLBACK.filter())
