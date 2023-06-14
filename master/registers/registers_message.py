from aiogram import types

from master.registers.parsers import exists_date
from master.registers.strings import Title, Msg
from master.registers import db
from master.registers import buttons


async def registers(message: types.Message):
    dates_registers = await db.get_registers_months(master_id=message.chat.id)
    if len(dates_registers) != 0:
        days_registers = await exists_date(master_id=message.chat.id, date=dates_registers[0])
        msg_text = Title.REGISTERS
        msg_btn = await buttons.registers_btn(date=dates_registers[0], registers_date=days_registers, count=len(dates_registers))
        await message.answer(text=msg_text, reply_markup=msg_btn)
    else:
        msg_text = f'{Title.REGISTERS}{Msg.NO_REGISTERS}'
        await message.answer(text=msg_text)
