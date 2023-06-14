from contextlib import suppress
from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import MessageNotModified

from bots import bot_client
from master.registers import db
from master.registers import buttons
from master.registers.callbacks import RegistersCallback
from master.registers.parsers import exists_date, registers_time, register_msg_builder, register_msg_builder_client, \
    register_msg_builder_client_db
from master.registers.strings import Title, Msg


async def time(query: types.CallbackQuery, date: datetime.date):
    registers_times = await db.get_registers_times(master_id=query.message.chat.id, date=date)
    schedule = await registers_time(master_id=query.message.chat.id, date=date, registers_times=registers_times)
    msg_text = f'{Title.REGISTERS}{date.strftime("%d.%m.%Y")}'
    msg_btn = await buttons.time_btn(registers=schedule)
    await query.message.edit_text(text=msg_text, reply_markup=msg_btn)


async def register(query: types.CallbackQuery, state: FSMContext):
    register_id = int(query.data.rstrip(RegistersCallback.REGISTER))
    register_data = await db.get_register_by_id(register_id=register_id)
    await state.update_data(id=register_id)
    msg_text = f'{Title.REGISTER}{await register_msg_builder(register=register_data)}'
    msg_btn = buttons.register_btn
    await query.message.edit_text(text=msg_text, reply_markup=msg_btn)


async def delete(query: types.CallbackQuery):
    await query.message.edit_reply_markup(reply_markup=buttons.confirm_delete_btn)


async def delete_confirm(query: types.CallbackQuery, state: FSMContext):
    register_id = (await state.get_data()).get('id')
    register = await db.get_register(register_id=register_id)
    await db.delete_register(register_id=register_id)
    msg_text = f"{Title.ABORT_REGISTER}{await register_msg_builder_client_db(register=register)}"
    await bot_client.edit_another_bot_message(chat_id=register[1], text=msg_text)
    date = datetime.strptime((await state.get_data()).get('date'), '%Y-%m-%d').date()
    registers_times = await db.get_registers_times(master_id=query.message.chat.id, date=date)

    if len(registers_times) != 0:
        schedule = await registers_time(
            master_id=query.message.chat.id,
            date=date,
            registers_times=registers_times
        )
        msg_text = f'{Title.REGISTERS}{date.strftime("%d.%m.%Y")}'
        msg_btn = await buttons.time_btn(registers=schedule)
        with suppress(MessageNotModified):
            await query.message.edit_text(text=msg_text, reply_markup=msg_btn)
    else:
        dates_registers = await db.get_registers_months(master_id=query.message.chat.id)
        if len(dates_registers) != 0:
            days_registers = await exists_date(master_id=query.message.chat.id, date=dates_registers[0])
            msg_text = Title.REGISTERS
            msg_btn = await buttons.registers_btn(date=dates_registers[0], registers_date=days_registers,
                                                  count=len(dates_registers))
            await query.message.edit_text(text=msg_text, reply_markup=msg_btn)
        else:
            msg_text = f'{Title.REGISTERS}{Msg.NO_REGISTERS}'
            await query.message.edit_text(text=msg_text)


async def cancel(query: types.CallbackQuery):
    await query.message.edit_reply_markup(reply_markup=buttons.register_btn)


async def back_to_date(query: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    date = datetime.strptime(state_data['date'], '%Y-%m-%d')
    dates_registers = await db.get_registers_months(master_id=query.message.chat.id)
    msg_text = Title.REGISTERS
    if len(dates_registers) != 0:
        msg_btn = await buttons.registers_btn(
            registers_date=await exists_date(master_id=query.message.chat.id, date=date),
            date=date.date(),
            index=state_data['index'],
            count=state_data['count'])
        await query.message.edit_text(text=msg_text, reply_markup=msg_btn)
    else:
        msg_text = f'{Title.REGISTERS}{Msg.NO_REGISTERS}'
        await query.message.edit_text(text=msg_text)


async def back_to_time(query: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    date = datetime.strptime(state_data['date'], '%Y-%m-%d').date()
    registers_times = await db.get_registers_times(master_id=query.message.chat.id, date=date)
    if len(registers_times) != 0:
        schedule = await registers_time(
            master_id=query.message.chat.id,
            date=date,
            registers_times=registers_times
        )
        msg_text = f'{Title.REGISTERS}{date.strftime("%d.%m.%Y")}'
        msg_btn = await buttons.time_btn(registers=schedule)
        await query.message.edit_text(text=msg_text, reply_markup=msg_btn)
    else:
        dates_registers = await db.get_registers_months(master_id=query.message.chat.id)
        if len(dates_registers) != 0:
            days_registers = await exists_date(master_id=query.message.chat.id, date=dates_registers[0])
            msg_text = Title.REGISTERS
            msg_btn = await buttons.registers_btn(date=dates_registers[0], registers_date=days_registers,
                                                  count=len(dates_registers))
            await query.message.edit_text(text=msg_text, reply_markup=msg_btn)
        else:
            msg_text = f'{Title.REGISTERS}{Msg.NO_REGISTERS}'
            await query.message.edit_text(text=msg_text)


async def date_selector(query: types.CallbackQuery, data: dict, state: FSMContext):
    callback = data['act']
    date = datetime.strptime(data['date'], '%Y-%m-%d').date()
    index_month = int(data['index'])
    months = await db.get_registers_months(master_id=query.message.chat.id)

    if callback.isdigit():
        date = date.replace(day=int(callback))
        await state.update_data(date=str(date), index=index_month, count=len(months))
        await time(query=query, date=date)

    if callback == RegistersCallback.PREV_MONTH:
        if index_month != 0:
            index_month -= 1
            registers_date = await exists_date(master_id=query.message.chat.id, date=months[index_month])
            await query.message.edit_reply_markup(
                reply_markup=await buttons.registers_btn(
                    date=months[index_month],
                    registers_date=registers_date,
                    count=len(months),
                    index=index_month)
            )
        else:
            await query.answer(cache_time=60)

    if callback == RegistersCallback.NEXT_MONTH:
        if index_month != len(months) - 1:
            index_month += 1
            registers_date = await exists_date(master_id=query.message.chat.id, date=months[index_month])
            await query.message.edit_reply_markup(
                reply_markup=await buttons.registers_btn(
                    date=months[index_month],
                    registers_date=registers_date,
                    count=len(months),
                    index=index_month)
            )
        else:
            await query.answer(cache_time=60)

    if callback == RegistersCallback.IGNORE:
        await query.answer(cache_time=60)
