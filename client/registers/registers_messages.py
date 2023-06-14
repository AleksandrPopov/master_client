from aiogram import types
from aiogram.dispatcher import FSMContext

import bots
from client.registers import db, buttons
from client.registers.strings import Title, Msg
from client.registers.parsers import registers_msg_builder


async def registers(message: types.Message, state: FSMContext):
    registers_db = await db.get_registers(client_id=message.chat.id)
    count_msg = message.message_id + 1
    if len(registers_db) != 0:
        for register in registers_db:
            msg_text = f'<b>{Title.YOUR_REGISTER}</b>\n\n{await registers_msg_builder(register=register)}'
            msg_btn = await buttons.delete_btn(register_id=register[0])
            await message.answer(text=msg_text, reply_markup=msg_btn)
            await bots.bot_client.add_messages(chat_id=message.chat.id, message_id=count_msg)
            count_msg += 1
    else:
        await message.answer(text=f"<b>{Title.REGISTERS}</b>\n\n{Msg.NO_REGISTERS}")
        await bots.bot_client.add_messages(chat_id=message.chat.id, message_id=count_msg)
