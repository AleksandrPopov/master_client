from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from client.registers.callbacks import RegistersCallback
from client.registers.strings import Btn


async def delete_btn(register_id: str) -> InlineKeyboardMarkup:
    btn = InlineKeyboardMarkup()
    btn.insert(InlineKeyboardButton(text=Btn.DELETE, callback_data=f'{register_id}{RegistersCallback.DELETE}'))
    return btn


delete_confirm = InlineKeyboardMarkup(row_width=2)
delete_confirm.insert(InlineKeyboardButton(text=Btn.YES, callback_data=RegistersCallback.DELETE_CONFIRM))
delete_confirm.insert(InlineKeyboardButton(text=Btn.NO, callback_data=RegistersCallback.CANCEL))
