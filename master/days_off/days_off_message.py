from aiogram import types
from aiogram.dispatcher import FSMContext

from master.days_off.buttons import days_off_btn
from master.days_off.strings import Title, Msg


async def days_off(message: types.Message, state: FSMContext):
    await state.update_data(master_id=message.chat.id, start=Msg.EMPTY_DAY, stop=Msg.EMPTY_DAY)
    msg_text = f'{Title.DAYS_OFF}{Msg.DISCRIPTION}'
    msg_btn = await days_off_btn(state=state)

    await message.answer(text=msg_text, reply_markup=msg_btn)
