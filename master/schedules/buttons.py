import datetime
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from master.schedules.strings import Btn
from master.schedules.callbacks import SchedulesCallback


async def add_schedule(start: datetime.time = datetime.time(hour=9, minute=0),
                       stop: datetime.time = datetime.time(hour=18, minute=0),
                       day: int = int(0)) -> InlineKeyboardMarkup:
    btn = InlineKeyboardMarkup(row_width=7)

    # Day selection.
    btn.row()
    for i in range(len(Btn.DAYS)):
        btn.insert(InlineKeyboardButton(text=Btn.DAYS[i], callback_data=SchedulesCallback.SCHEDULES_CALLBACK.new(
            str(i), start, stop, day)))

    # Top row buttons. BUTTONS: "↑", "↑", "↑", "↑".
    btn.row()
    for i in SchedulesCallback.row_1:
        btn.insert(InlineKeyboardButton(text=i[0], callback_data=SchedulesCallback.SCHEDULES_CALLBACK.new(
            i[1], start, stop, day)))

    # Selected schedule time.
    btn.row()
    btn.insert(InlineKeyboardButton(text=start.strftime('%H'), callback_data=SchedulesCallback.SCHEDULES_CALLBACK.new(
        SchedulesCallback.IGNORE, start, stop, day)))
    btn.insert(InlineKeyboardButton(text=start.strftime('%M'), callback_data=SchedulesCallback.SCHEDULES_CALLBACK.new(
        SchedulesCallback.IGNORE, start, stop, day)))
    btn.insert(InlineKeyboardButton(text=Btn.DASH, callback_data=SchedulesCallback.SCHEDULES_CALLBACK.new(
        SchedulesCallback.IGNORE, start, stop, day)))
    btn.insert(InlineKeyboardButton(text=stop.strftime('%H'), callback_data=SchedulesCallback.SCHEDULES_CALLBACK.new(
        SchedulesCallback.IGNORE, start, stop, day)))
    btn.insert(InlineKeyboardButton(text=stop.strftime('%M'), callback_data=SchedulesCallback.SCHEDULES_CALLBACK.new(
        SchedulesCallback.IGNORE, start, stop, day)))

    # Bottom row buttons. BUTTONS: "↓", "↓", "↓", "↓".
    btn.row()
    for i in SchedulesCallback.row_3:
        btn.insert(InlineKeyboardButton(text=i[0], callback_data=SchedulesCallback.SCHEDULES_CALLBACK.new(
            i[1], start, stop, day)))

    # Time or day off selection. BUTTONS: "Add", "Day off"
    btn.row()
    btn.insert(InlineKeyboardButton(text=Btn.DAY_OFF, callback_data=SchedulesCallback.SCHEDULES_CALLBACK.new(
        SchedulesCallback.DAY_OFF, start, stop, day)))

    return btn
