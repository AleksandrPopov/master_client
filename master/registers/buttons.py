from datetime import datetime

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from master.registers.callbacks import RegistersCallback
from master.registers.strings import Btn


async def registers_btn(date: datetime.date, registers_date: list, count: int = 0, index: int = 0) -> InlineKeyboardMarkup:

    btn = InlineKeyboardMarkup(row_width=7)
    ignore_callback = RegistersCallback.REGISTERS_CALLBACK.new(RegistersCallback.IGNORE, date, count, index)

    btn.row()
    for day_short in Btn.DAYS:
        btn.insert(InlineKeyboardButton(day_short, callback_data=ignore_callback))

    btn.row()
    for day in registers_date:
        callback = RegistersCallback.REGISTERS_CALLBACK.new(str(day), date, count, index)
        if day == 0:
            day = ' '
            callback = ignore_callback
        btn.insert(InlineKeyboardButton(text=str(day), callback_data=callback))

    btn.row()
    if index == 0:
        btn.insert(InlineKeyboardButton(
            text=" ",
            callback_data=ignore_callback))
    else:
        btn.insert(InlineKeyboardButton(
            text="<",
            callback_data=RegistersCallback.REGISTERS_CALLBACK.new(RegistersCallback.PREV_MONTH, date, count, index)))

    btn.insert(InlineKeyboardButton(f'{Btn.MONTHS[date.month]} {date.year}', callback_data=ignore_callback))

    if count - 1 == index:
        btn.insert(InlineKeyboardButton(
            text=" ",
            callback_data=ignore_callback))
    else:
        btn.insert(InlineKeyboardButton(
            text=">",
            callback_data=RegistersCallback.REGISTERS_CALLBACK.new(RegistersCallback.NEXT_MONTH, date, count, index)))
    return btn


async def time_btn(registers: list) -> InlineKeyboardMarkup:
    btn = InlineKeyboardMarkup(row_width=3)
    for register in registers:
        if register['time'] == register['time'].min:
            btn.insert(InlineKeyboardButton(text=' ', callback_data=RegistersCallback.IGNORE))
        else:
            btn.insert(InlineKeyboardButton(
                text=register['time'].strftime('%H:%M'),
                callback_data=f"{register['id']}{RegistersCallback.REGISTER}")
            )
    btn.row()
    btn.insert(InlineKeyboardButton(text=Btn.BACK, callback_data=RegistersCallback.BACK_TO_DATE))
    return btn

# MENU: "Delete register". BUTTONS: "Delete", "Back".
register_btn = InlineKeyboardMarkup(row_width=1)
register_btn.insert(InlineKeyboardButton(text=Btn.DELETE, callback_data=RegistersCallback.DELETE))
register_btn.insert(InlineKeyboardButton(text=Btn.BACK, callback_data=RegistersCallback.BACK_TO_TIME))


# MENU: "Delete register". BUTTONS: "Yes", "No", "Back".
confirm_delete_btn = InlineKeyboardMarkup(row_width=2)
confirm_delete_btn.insert(InlineKeyboardButton(text=Btn.YES, callback_data=RegistersCallback.DELETE_CONFIRM))
confirm_delete_btn.insert(InlineKeyboardButton(text=Btn.NO, callback_data=RegistersCallback.CANCEL))
confirm_delete_btn.row()
confirm_delete_btn.insert(InlineKeyboardButton(text=Btn.BACK, callback_data=RegistersCallback.BACK_TO_TIME))
