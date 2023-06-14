from contextlib import suppress

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentTypes
from aiogram.utils.exceptions import MessageToDeleteNotFound, MessageCantBeDeleted

from master.account.callbacks import AccountCallback, StartCommand
from master.categories.callbacks import CategoriesCallback
from master.days_off.callbacks import DaysOffCallback
from master.registers.callbacks import RegistersCallback
from master.schedules.callbacks import SchedulesCallback
from master.services.callbacks import ServicesCallback


async def close(message: types.Message, state: FSMContext):
    commands_list = [
        StartCommand.START,
        AccountCallback.ACCOUNT,
        RegistersCallback.REGISTER,
        SchedulesCallback.SCHEDULES,
        DaysOffCallback.DAYS_OFF,
        CategoriesCallback.CATEGORIES,
        ServicesCallback.SERVICES
    ]
    if await state.get_state() is None or message.text[1:] not in commands_list:
        with suppress(MessageToDeleteNotFound, MessageCantBeDeleted):
            await message.delete()


async def register_filter_handler(dp: Dispatcher):
    dp.register_message_handler(close, content_types=ContentTypes.ANY)
