from aiogram import types
from aiogram.dispatcher import FSMContext

from bots import bot_master
from config import COUNTRY, COUNTS_MASTERS

from master.account import db
from master.account.state import AccountState
from master.account.strings import Title, Msg
from master.account.buttons import account_menu, btn_get_contact
from master.account.parsers import msg_builder, format_contact
from master import parse


async def start(message: types.Message):
    master = await db.get_master(master_id=message.chat.id)
    if master is not None:
        await message.answer(text=f"<b>{master[0][0]}</b>{Msg.HELLO}")
    elif master is not None or COUNTS_MASTERS > await db.get_counts_masters():
        await message.answer(text=Msg.ADD_MASTER, reply_markup=btn_get_contact)
    else:
        await message.answer("Nope")


async def account(message: types.Message):
    master = await db.get_master(master_id=message.chat.id)
    if master is not None:
        msg_text = f'{Title.ACCOUNT}{await msg_builder(name=master[0], contact=master[1])}'
        await message.answer(text=msg_text, reply_markup=account_menu)
    else:
        await start(message=message)


async def add_master(message: types.Message):
    contact = await format_contact(contact=message.contact.phone_number, country=COUNTRY)
    # TODO: Check number.
    await db.add_master(
        master_id=message.chat.id,
        master_name=message.from_user.first_name,
        master_contact=contact
    )
    await account(message=message)


async def change_name(message: types.Message, state: FSMContext):
    name = await parse.format_name(name=message.text)
    if name is not False:
        master = await db.change_master_name(master_id=message.chat.id, name=name)
        msg_text = f'{Title.ACCOUNT}{await msg_builder(name=master[0], contact=master[1])}'
        await bot_master.edit_messages(message=message, text=msg_text, btn=account_menu)
        await state.finish()
    else:
        msg_text = f'{Title.ACCOUNT}{Msg.ERROR_NAME}'
        await bot_master.edit_messages(message=message, text=msg_text)
        await AccountState.change_name.set()


async def change_contact(message: types.Message, state: FSMContext):
    contact = await format_contact(contact=message.text, country=COUNTRY)
    if contact is not False:
        await db.change_master_contact(master_id=message.chat.id, contact=contact)
        master = await db.get_master(master_id=message.chat.id)
        msg_text = f'{Title.ACCOUNT}{await msg_builder(name=master[0], contact=master[1])}'
        await bot_master.edit_messages(message=message, text=msg_text, btn=account_menu)
        await state.finish()
    else:
        msg_text = f'{Title.ACCOUNT}{Msg.ERROR_CONTACT}'
        await bot_master.edit_messages(message=message, text=msg_text)
        await AccountState.change_contact.set()
