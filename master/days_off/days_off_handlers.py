from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from bots import bot_master
from master.days_off.callbacks import DaysOffCallback
from master.days_off import days_off_query
from master.days_off import days_off_message


async def days_off_command(message: types.Message, state: FSMContext):
    await state.finish()
    await bot_master.del_messages(message=message)
    await days_off_message.days_off(message=message, state=state)


async def days_off_query_handler(query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await days_off_query.days_off_selector(query=query, data=callback_data, state=state)


async def register_days_off_handlers(dp: Dispatcher):
    dp.register_message_handler(days_off_command, commands=[DaysOffCallback.DAYS_OFF])
    dp.register_callback_query_handler(days_off_query_handler, DaysOffCallback.DAYS_OFF_CALLBACK.filter())
