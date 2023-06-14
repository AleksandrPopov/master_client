from calendar import monthrange
from contextlib import suppress
from datetime import datetime, timedelta

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import MessageNotModified

from config import TZ
from master.days_off import db
from master.days_off.buttons import days_off_btn
from master.days_off.callbacks import DaysOffCallback
from master.days_off.strings import Msg


async def days_off_selector(query: types.CallbackQuery, data: dict, state: FSMContext):
    date_now = datetime.now(TZ).date()
    callback = data.get('act')
    date = datetime.strptime(data.get('date'), '%Y-%m-%d').date()
    days_off = data.get('days_off')
    start = (await state.get_data()).get('start')
    stop = (await state.get_data()).get('stop')
    registers = []

    # Day off
    if callback == DaysOffCallback.SELECT_DAY:
        # Check empty second day.
        if start == Msg.EMPTY_DAY or date < datetime.strptime(start, '%d.%m.%Y').date():
            registers = await db.get_registers(
                master_id=query.message.chat.id,
                start_date=date,
                stop_date=date
            )
            start = date.strftime('%d.%m.%Y')
            stop = Msg.EMPTY_DAY
        else:
            registers = await db.get_registers(
                master_id=query.message.chat.id,
                start_date=datetime.strptime(start, '%d.%m.%Y').date(),
                stop_date=date
            )
            stop = date.strftime('%d.%m.%Y')

        # Check registers
        if len(registers) == 0:
            await state.update_data(start=start, stop=stop)
            with suppress(MessageNotModified):
                await query.message.edit_reply_markup(await days_off_btn(date=date, days_off=days_off, state=state))
        else:
            msg_text = ''
            check_date = datetime.min.date()
            for register in registers:
                if register.date() != check_date:
                    msg_text += f'{register.date().strftime("%d.%m.%Y")}: {register.time().strftime("%H:%M")}'
                else:
                    msg_text += f', {register.time().strftime("%H:%M")}\n'
                check_date = register.date()
            await query.answer(text=msg_text, show_alert=True)
    else:
        # Previous month
        if callback == DaysOffCallback.PREV_MONTH:
            if date_now.replace(day=1) == date.replace(day=1):
                callback = DaysOffCallback.IGNORE
            else:
                days = monthrange(int(date.year), int(date.month))[1]
                date = date.replace(day=days) - timedelta(days=days)

        # Next month
        if callback == DaysOffCallback.NEXT_MONTH:
            days = monthrange(int(date.year), int(date.month))[1]
            date = date.replace(day=1) + timedelta(days=days)

        # Add day off
        if callback == DaysOffCallback.ADD:
            if start == Msg.EMPTY_DAY:
                await query.answer(text=Msg.ALERT_EMPTY_START_DAY, show_alert=True)
            else:
                if start != Msg.EMPTY_DAY and stop == Msg.EMPTY_DAY:
                    stop = start
                await db.add_day_off(
                    master_id=query.message.chat.id,
                    start_date=datetime.strptime(start, '%d.%m.%Y').date(),
                    stop_date=datetime.strptime(stop, '%d.%m.%Y').date()
                )
                start = Msg.EMPTY_DAY
                stop = Msg.EMPTY_DAY

        # Clear days off selection field
        if callback == DaysOffCallback.CLEAR:
            start = Msg.EMPTY_DAY
            stop = Msg.EMPTY_DAY

        # Delete days off
        if callback == DaysOffCallback.DELETE:
            days_off_start = datetime.strptime(days_off.split(' - ')[0], '%d.%m.%Y').date()
            days_off_stop = days_off.split(' - ')[0] if len(days_off.split(' - ')) != 2 else days_off.split(' - ')[1]
            days_off_stop = datetime.strptime(days_off_stop, '%d.%m.%Y').date()
            await db.delete_days_off(master_id=query.message.chat.id, start_date=days_off_start,
                                     stop_date=days_off_stop)

        # Cancel deletion
        if callback == DaysOffCallback.CANCEL:
            days_off = ''

        if callback == DaysOffCallback.IGNORE:
            await query.answer(cache_time=60)

        await state.update_data(start=start, stop=stop)
        with suppress(MessageNotModified):
            await query.message.edit_reply_markup(await days_off_btn(date=date, days_off=days_off, state=state))
