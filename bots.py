import asyncio

from aiogram import Dispatcher
from aiogram.types import BotCommand

from classes.Storage import BotStorage
from classes.TBots import TBot
from client.add_register.callbacks import AddRegisterCallback
from client.contacts.callbacks import ContactsCallback
from client.registers.callbacks import RegistersCallback as Client

from client.contacts.strings import Title
from config import TOKEN_MASTER, TOKEN_CLIENT
from master.categories.callbacks import CategoriesCallback
from master.registers.callbacks import RegistersCallback

from master.days_off.callbacks import DaysOffCallback
from master.schedules.callbacks import SchedulesCallback
from master.services.callbacks import ServicesCallback
from master.account.callbacks import AccountCallback, StartCommand
from master.registers.strings import Command as Registers
from master.schedules.strings import Command as Schedules
from master.days_off.strings import Command as DaysOff
from master.categories.strings import Command as Categories
from master.services.strings import Command as Services
from master.account.strings import Command as Account

bot_master = TBot(token=TOKEN_MASTER, parse_mode='HTML', loop=asyncio.get_event_loop(), role='master')
bot_client = TBot(token=TOKEN_CLIENT, parse_mode='HTML', loop=asyncio.get_event_loop(), role='client')

dp_master = Dispatcher(bot=bot_master, storage=BotStorage(role='master'))
dp_client = Dispatcher(bot=bot_client, storage=BotStorage(role='client'))


async def commands_master():
    await bot_master.set_my_commands([
        BotCommand(StartCommand.START, 'Старт'),
        BotCommand(RegistersCallback.REGISTERS, Registers.REGISTERS),
        BotCommand(SchedulesCallback.SCHEDULES, Schedules.SCHEDULES),
        BotCommand(DaysOffCallback.DAYS_OFF, DaysOff.DAYS_OFF),
        BotCommand(CategoriesCallback.CATEGORIES, Categories.CATEGORIES),
        BotCommand(ServicesCallback.SERVICES, Services.SERVICES),
        BotCommand(AccountCallback.ACCOUNT, Account.ACCOUNT)
    ])


async def commands_client():
    await bot_client.set_my_commands([
        BotCommand(AddRegisterCallback.START, 'Старт'),
        BotCommand(Client.REGISTERS, Registers.REGISTERS),
        BotCommand(ContactsCallback.CONTACTS, Title.CONTACTS)
    ])
