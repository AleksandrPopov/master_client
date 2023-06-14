from bots import bot_client
from client.registers.db import get_register_incoming, delete_register_after
from client.registers.strings import Title

from master.registers.parsers import register_msg_builder_client_db


async def register_incoming():
    registers = await get_register_incoming()
    if registers is not None:
        for register in registers:
            msg_text = f'{Title.INCOMING_REGISTER}{await register_msg_builder_client_db(register)}'
            await bot_client.edit_another_bot_message(chat_id=register[1], text=msg_text)


async def delete_register():
    await delete_register_after()
