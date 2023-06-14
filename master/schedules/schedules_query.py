from contextlib import suppress
from datetime import timedelta
from datetime import datetime

from aiogram import types
from aiogram.utils.exceptions import MessageNotModified

from master.schedules import db
from master.schedules.strings import Title, Msg
from master.schedules.buttons import add_schedule
from master.schedules.parsers import schedule_msg
from master.schedules.callbacks import SchedulesCallback


async def schedules_selector(query: types.CallbackQuery, data: dict):
    callback = data.get('act')
    day = int(callback) if callback.isdigit() else int(data.get('day'))
    schedule = await db.get_schedule_day(master_id=query.message.chat.id, day=day)
    date = datetime.now().min

    start_db = datetime.combine(date.date().min, schedule[0])
    stop_db = datetime.combine(date.date().min, schedule[1])

    start = datetime.strptime(data.get('start'), '%H:%M:%S')
    stop = datetime.strptime(data.get('stop'), '%H:%M:%S')

    start_time = datetime.strptime('09:00:00', '%H:%M:%S').time()
    stop_time = datetime.strptime('18:00:00', '%H:%M:%S').time()

    if callback == SchedulesCallback.IGNORE:
        with suppress(MessageNotModified):
            await query.answer(cache_time=60)

    if callback.isdigit():
        start = start_db
        stop = stop_db

    if callback == SchedulesCallback.DAY_OFF:
        start = start.min
        stop = stop.min

    if callback == SchedulesCallback.START_UP_HOUR:
        start += timedelta(hours=1)

    if callback == SchedulesCallback.START_DOWN_HOUR:
        start -= timedelta(hours=1)

    if callback == SchedulesCallback.START_UP_MIN:
        start += timedelta(minutes=30)

    if callback == SchedulesCallback.START_DOWN_MIN:
        start -= timedelta(minutes=30)

    if callback == SchedulesCallback.STOP_UP_HOUR:
        stop += timedelta(hours=1)

    if callback == SchedulesCallback.STOP_DOWN_HOUR:
        stop -= timedelta(hours=1)

    if callback == SchedulesCallback.STOP_UP_MIN:
        stop += timedelta(minutes=30)

    if callback == SchedulesCallback.STOP_DOWN_MIN:
        stop -= timedelta(minutes=30)

    if date.time() != start.time() < stop.time() != date.time() or start.time() == date.time() == stop.time():
        if date.time() == start_db.time() == start.time() and date.time() == stop_db.time() == stop.time():
            start = datetime.combine(date.date(), start_time)
            stop = datetime.combine(date.date(), stop_time)
        await db.change_schedule_day(master_id=query.message.chat.id, day=day, start=start.time(), stop=stop.time())
        with suppress(MessageNotModified):
            await query.message.edit_text(f"{Title.SCHEDULES}{Msg.SCHEDULES}\n"
                                          f"{await schedule_msg(master_id=query.message.chat.id, day=day)}")
            await query.message.edit_reply_markup(await add_schedule(start=start.time(), stop=stop.time(), day=day))
    else:
        await query.answer(text='Nope', show_alert=True)
