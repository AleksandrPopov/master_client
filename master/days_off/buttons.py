from datetime import datetime

from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from master.days_off import db
from master.days_off.callbacks import DaysOffCallback
from master.days_off.parsers import get_days_off, days_off_parse
from master.days_off.strings import Btn
from config import TZ


async def days_off_btn(
        date: datetime.date = datetime.now(TZ).date(),
        days_off: str = '',
        clear_state: bool = False,
        state: FSMContext = None
) -> InlineKeyboardMarkup:
    days_off_db = await db.get_days_off(master_id=(await state.get_data()).get('master_id'))
    date_now = datetime.now(TZ).date()
    start = (await state.get_data()).get('start')
    stop = (await state.get_data()).get('stop')

    if clear_state:
        await state.finish()

    # Days off list.
    inline_kb = InlineKeyboardMarkup(row_width=7)
    if len(days_off_db) != 0:
        for day_off in await days_off_parse(days_off_db=days_off_db):
            if day_off == days_off:
                inline_kb.row()
                inline_kb.insert(InlineKeyboardButton(Btn.DELETE,
                                                      callback_data=DaysOffCallback.DAYS_OFF_CALLBACK.new(
                                                          DaysOffCallback.DELETE, date, day_off)))
                inline_kb.insert(InlineKeyboardButton(Btn.NO,
                                                      callback_data=DaysOffCallback.DAYS_OFF_CALLBACK.new(
                                                          DaysOffCallback.CANCEL, date, day_off)))
            if day_off != days_off:
                inline_kb.row()
                inline_kb.insert(InlineKeyboardButton(text=day_off,
                                                      callback_data=DaysOffCallback.DAYS_OFF_CALLBACK.new(
                                                          DaysOffCallback.DAYS_OFF, date, day_off)))
    inline_kb.row()
    inline_kb.insert(InlineKeyboardButton(f'{start} - {stop}' if start != stop else f'{start}',
                                          callback_data=DaysOffCallback.IGNORE))
    inline_kb.row()

    for week_days in Btn.DAYS:
        inline_kb.insert(InlineKeyboardButton(text=week_days, callback_data=DaysOffCallback.IGNORE))

    for week in await get_days_off(start=start, stop=stop, date=date, days_off_db=days_off_db):
        inline_kb.row()
        for calendar_days in week:
            if calendar_days == 0 or calendar_days < date_now.day and date.replace(day=1) == date_now.replace(day=1):
                inline_kb.insert(InlineKeyboardButton(Btn.EMPTY, callback_data=DaysOffCallback.IGNORE))
                continue
            date = date.replace(day=calendar_days)
            inline_kb.insert(InlineKeyboardButton(str(calendar_days),
                                                  callback_data=DaysOffCallback.DAYS_OFF_CALLBACK.new(
                                                      DaysOffCallback.SELECT_DAY, date, days_off)))
    inline_kb.row()
    symbol = Btn.EMPTY if date.replace(day=1) == date_now.replace(day=1) else Btn.PREV

    inline_kb.insert(InlineKeyboardButton(
        symbol, callback_data=DaysOffCallback.DAYS_OFF_CALLBACK.new(DaysOffCallback.PREV_MONTH, date, days_off)))

    inline_kb.insert(InlineKeyboardButton(text=Btn.MONTHS[date.month],
                                          callback_data=DaysOffCallback.IGNORE))
    inline_kb.insert(InlineKeyboardButton(Btn.NEXT,
                                          callback_data=DaysOffCallback.DAYS_OFF_CALLBACK.new(
                                              DaysOffCallback.NEXT_MONTH, date, days_off)
                                          ))
    inline_kb.row()
    inline_kb.insert(InlineKeyboardButton(
        Btn.ADD, callback_data=DaysOffCallback.DAYS_OFF_CALLBACK.new(DaysOffCallback.ADD, date, days_off)
    ))
    inline_kb.insert(InlineKeyboardButton(
        Btn.CLEAR, callback_data=DaysOffCallback.DAYS_OFF_CALLBACK.new(DaysOffCallback.CLEAR, date, days_off)
    ))
    return inline_kb
