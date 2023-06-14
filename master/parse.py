import re

from aiogram import types
from aiogram.dispatcher import FSMContext

from bots import bot_master
from master.account.account_handlers import account_command
from master.account.account_message import start
from master.account.callbacks import AccountCallback, StartCommand
from master.categories.callbacks import CategoriesCallback
from master.categories import categories_handlers
from master.days_off.callbacks import DaysOffCallback
from master.days_off.days_off_handlers import days_off_command
from master.registers.callbacks import RegistersCallback
from master.registers import registers_handlers
from master.schedules.callbacks import SchedulesCallback
from master.schedules.schedules_handlers import schedules_command
from master.services.callbacks import ServicesCallback

from master.services.services_handlers import services_command


async def state_cleaner(message: types.Message, state: FSMContext):
    if message.text[1:] == StartCommand.START:
        await state.finish()
        await bot_master.del_messages(message=message)
        await start(message=message)

    if message.text[1:] == RegistersCallback.REGISTERS:
        await state.finish()
        await bot_master.del_messages(message=message)
        await registers_handlers.registers_command(message=message, state=state)

    if message.text[1:] == SchedulesCallback.SCHEDULES:
        await state.finish()
        await bot_master.del_messages(message=message)
        await schedules_command(message=message, state=state)

    if message.text[1:] == DaysOffCallback.DAYS_OFF:
        await state.finish()
        await bot_master.del_messages(message=message)
        await days_off_command(message=message, state=state)

    if message.text[1:] == CategoriesCallback.CATEGORIES:
        await state.finish()
        await bot_master.del_messages(message=message)
        await categories_handlers.categories_command(message=message, state=state)

    if message.text[1:] == ServicesCallback.SERVICES:
        await state.finish()
        await bot_master.del_messages(message=message)
        await services_command(message=message, state=state)

    if message.text[1:] == AccountCallback.ACCOUNT:
        await state.finish()
        await bot_master.del_messages(message=message)
        await account_command(message=message, state=state)


async def format_name(name: str) -> str | bool:
    """
    Remove unnecessary substrings and spaces.
    Checking the size of a string in bytes.

    :param
    :return:
    """
    name = name.lstrip(" ").rstrip(" ").lower()
    name = re.sub(" +", " ", name)
    name = re.sub("[<|>]", "", name).capitalize()
    if 64 > len(name.encode("utf-8")) != 0:
        return name
    else:
        return False
