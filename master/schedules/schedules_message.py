from aiogram import types

from client.add_register.db import get_master
from master.account.account_message import start

from master.schedules.strings import Title, Msg
from master.schedules import parsers
from master.schedules import buttons


async def schedules(message: types.Message):
    master = await get_master(master_id=message.chat.id)
    if len(master) != 0:
        await message.answer(text=f"{Title.SCHEDULES}{Msg.SCHEDULES}\n"
                                  f"{await parsers.schedule_msg(master_id=message.chat.id)}",
                             reply_markup=await buttons.add_schedule())
    else:
        await start(message=message)
