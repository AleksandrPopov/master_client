from aiogram import types
from aiogram.dispatcher import FSMContext

from master.account import account_handlers
from master.account import db
from master.account.callbacks import StartCommand
from master.account.parsers import msg_builder
from master.account.state import AccountState
from master.account.strings import Title, Msg
from master.account.buttons import btn_delete_confirm, account_menu


async def change_name(query: types.CallbackQuery):
    msg_text = f'{Title.ACCOUNT}{Msg.ENTER_NEW_NAME}'
    await query.message.edit_text(text=msg_text)
    await AccountState.change_name.set()


async def change_contact(query: types.CallbackQuery):
    msg_text = f'{Title.ACCOUNT}{Msg.ENTER_NEW_CONTACT}'
    await query.message.edit_text(text=msg_text)
    await AccountState.change_contact.set()


async def delete(query: types.CallbackQuery):
    msg_text = f'{Title.ACCOUNT}{Msg.DELETE}'
    msg_btn = btn_delete_confirm
    await query.message.edit_text(text=msg_text, reply_markup=msg_btn)


async def cancel(query: types.CallbackQuery):
    master = await db.get_master(master_id=query.message.chat.id)
    if len(master) != 0:
        msg_text = f'{Title.ACCOUNT}{await msg_builder(name=master[0], contact=master[1])}'
        await query.message.edit_text(text=msg_text, reply_markup=account_menu)


async def delete_confirm(query: types.CallbackQuery, state: FSMContext):
    await db.delete_account(master_id=query.message.chat.id)
    query.message.text = f'/{StartCommand.START}'
    await account_handlers.account_command(message=query.message, state=state)
