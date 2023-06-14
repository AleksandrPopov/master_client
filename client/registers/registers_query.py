from aiogram import types
from aiogram.dispatcher import FSMContext

import bots
from client.registers import db, buttons
from client.registers.callbacks import RegistersCallback
from client.registers.strings import Title
from master.registers.db import get_register_by_id
from master.registers.parsers import register_msg_builder


async def delete_registers(query: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    query_data = query.data.rstrip(RegistersCallback.DELETE_CONFIRM)
    registers_id = int(query_data) if query_data.isdigit() else state_data.get('reg_id')
    if isinstance(state_data.get('reg_id'), int):
        await bots.bot_client.edit_message_reply_markup(
            chat_id=query.message.chat.id,
            message_id=state_data['msg_id'],
            reply_markup=await buttons.delete_btn(register_id=state_data['reg_id'])
        )
    await query.message.edit_reply_markup(reply_markup=buttons.delete_confirm)
    await state.update_data(
        reg_id=registers_id,
        msg_id=query.message.message_id,
    )


async def delete_cancel(query: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    await bots.bot_client.edit_message_reply_markup(
        chat_id=query.message.chat.id,
        message_id=state_data['msg_id'],
        reply_markup=await buttons.delete_btn(register_id=state_data['reg_id'])
    )


async def delete_confirm(query: types.CallbackQuery, state: FSMContext):
    state_date = await state.get_data()
    register = await get_register_by_id(register_id=state_date.get('reg_id'))
    msg_text = f"{Title.ABORT_REGISTER}{await register_msg_builder(register=register)}"
    await db.delete_register(register_id=state_date.get('reg_id'))
    await bots.bot_client.delete_message(chat_id=query.message.chat.id, message_id=state_date['msg_id'])
    await bots.bot_master.edit_another_bot_message(chat_id=register[1], text=msg_text)
    await state.update_data(reg_id='', msg_id='')
