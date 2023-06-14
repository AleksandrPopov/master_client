from calendar import monthrange
from contextlib import suppress
from datetime import datetime, timedelta

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import MessageNotModified

import bots
from config import TZ
from client.add_register import buttons, db
from client.add_register.add_register_message import categories_message, services_message, start, \
    more_services_messages, date_message, time_messages, contact_messages
from client.add_register.callbacks import AddRegisterCallback
from client.add_register.parsers import add_register_msg_builder, price_msg_builder, \
    time_summ, cost_minus, cost_summ
from client.add_register.states import AddRegisterState
from client.add_register.strings import Title, Msg
from master.registers.parsers import register_msg_builder_client


async def categories(query: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    start_state = state_data.get('start')
    master_id = query.data.rstrip(AddRegisterCallback.CATEGORY)

    if master_id.isdigit():
        master_id = int(master_id)
        master_db = await db.get_master(master_id=master_id)
        await state.update_data(master=list(master_db))
    else:
        master_id = state_data.get('master')[0]

    categories_db = await db.get_categories(master_id=master_id)
    categories_state = len(state_data.get('categories'))

    await categories_message(
        message=query.message,
        state=state_data,
        categories_db=categories_db,
        back='more_services' if categories_state != 0 else None if start_state == 'categories' else 'masters'
    )


async def services(query: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    category_id = query.data.rstrip(AddRegisterCallback.SERVICE)
    category_id = int(category_id) if category_id.isdigit() else int(state_data.get('categories')[-1]['id'])
    services_db = await db.get_services(category_id=category_id)
    category_db = await db.get_category(category_id=category_id)

    categories_state = state_data.get('categories')
    categories_state.append(list(category_db))
    await state.update_data(categories=categories_state)

    await services_message(
        message=query.message,
        state=state_data,
        services_db=services_db)


async def more_services(query: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    service_id = int(query.data.rstrip(AddRegisterCallback.MORE))
    service_db = (await db.get_service(service_id=service_id))
    services_state = state_data.get('services')
    services_state.append(list(service_db))
    cost = await cost_summ(services_state)
    print('----------------------------------', services_state)
    await state.update_data(services=services_state, cost=cost)
    await more_services_messages(message=query.message, state=await state.get_data())


async def date(query: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    msg_btn = await buttons.date(master_id=state_data['master'][0], services_list=state_data['services'])

    await date_message(message=query.message, state=state_data, btn=msg_btn)


async def date_selector(query: types.CallbackQuery, state: FSMContext, data: dict):
    state_data = await state.get_data()
    date_now = datetime.now(TZ).date()
    date_current = datetime.strptime(data['date'], '%Y-%m-%d').date()

    if data['act'] == AddRegisterCallback.NEXT_MONTH:
        days = monthrange(int(date_current.year), int(date_current.month))[1]
        date_current = date_current.replace(day=1) + timedelta(days=days)

    if data['act'] == AddRegisterCallback.PREV_MONTH:
        if date_now.replace(day=1) == date_current.replace(day=1):
            data['act'] = AddRegisterCallback.IGNORE
        else:
            days = monthrange(int(date_current.year), int(date_current.month))[1]
            date_current = date_current.replace(day=days) - timedelta(days=days)

    if data['act'] == AddRegisterCallback.IGNORE:
        await query.answer(cache_time=60)

    with suppress(MessageNotModified):
        await query.message.edit_reply_markup(await buttons.date(
            master_id=state_data['master'][0],
            date_current=date_current,
            services_list=state_data.get('services'))
        )


async def time(query: types.CallbackQuery, state: FSMContext):
    date_current = datetime.strptime(query.data.rstrip(AddRegisterCallback.TIME), '%Y-%m-%d').date()
    await state.update_data(date=str(date_current))
    await time_messages(message=query.message, state=await state.get_data())


async def contact(query: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    checked_time = datetime.strptime(query.data.rstrip(AddRegisterCallback.CONTACT), '%H:%M')
    stop_date = await time_summ(date=checked_time, services=state_data['services'])
    await state.update_data(start_time=checked_time.time().strftime('%H:%M'), stop_time=stop_date)
    await contact_messages(message=query.message, state=await state.get_data())


async def confirm_register(query: types.CallbackQuery, state: FSMContext):
    client_id = int(query.data.rstrip(AddRegisterCallback.CONFIRM_REGISTER))
    client_db = await db.get_client(client_id=client_id)
    await state.update_data(client=list(client_db))
    msg_text = f"<b>{Title.CONFIRM_REGISTER}</b>\n\n{await add_register_msg_builder(state=await state.get_data())}"
    msg_btn = await buttons.confirm_register()
    await query.message.edit_text(text=msg_text, reply_markup=msg_btn)


async def add_register_to_db(query: types.CallbackQuery, state: FSMContext):
    state_date = await state.get_data()
    await db.add_register(state=await state.get_data())
    msg_text = f"<b>{Title.YOUR_REGISTER}</b>\n\n{await add_register_msg_builder(state=state_date)}"
    msg_text_master = await register_msg_builder_client(state=state_date)
    await bots.bot_client.edit_messages(message=query.message, text=msg_text)
    await bots.bot_master.edit_another_bot_message(chat_id=state_date['master'][0], text=msg_text_master)


async def price(query: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    master_id = state_data.get('master')
    category_id = True if state_data.get('category_id') is not None else False

    msg_title = f'<b>{Title.PRICE}</b>\n'
    msg_text = f'{await price_msg_builder(master_id=master_id[0])}'
    msg_btn = await buttons.price_list(callback=category_id)
    await query.message.edit_text(text=f'{msg_title}{msg_text}', reply_markup=msg_btn)


async def add_contact(query: types.CallbackQuery, state: FSMContext):
    await query.message.edit_text(text=f"<b>{Title.CONTACTS}</b>\n\n{Msg.SET_NAME}")
    await AddRegisterState.add_contact_name.set()


async def back_to_masters(query: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await bots.bot_client.del_messages(message=query.message)
    await start(message=query.message, state=state)


async def back_to_categories(query: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    master_id = state_data.get('master')[0]
    categories_state = state_data.get('categories')
    categories_db = await db.get_categories(master_id=master_id)
    del categories_state[-1]
    await state.update_data(categories=categories_state)

    await categories_message(
        message=query.message,
        state=state_data,
        categories_db=categories_db,
        back='more_services' if len(categories_state) != 0 else 'masters' if state_data['start'] == 'masters' else None
    )


async def back_to_services(query: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    category_id = state_data.get('categories')[-1][0]
    services_state = state_data.get('services')
    services_db = await db.get_services(category_id=category_id)
    cost = await cost_minus(
        cost=int(state_data.get('cost')),
        cost_service=int(services_state[-1][2])
    )
    del services_state[-1]
    await state.update_data(services=services_state, cost=cost)

    await services_message(
        message=query.message,
        state=await state.get_data(),
        services_db=services_db
    )


async def back_to_more_services(query: types.CallbackQuery, state: FSMContext):
    await more_services_messages(message=query.message, state=await state.get_data())


async def back_to_date(query: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    msg_btn = await buttons.date(
        master_id=state_data['master'][0],
        services_list=state_data['services'],
        date_current=datetime.strptime(state_data.pop('date'), '%Y-%m-%d').date()
    )
    await state.update_data(date='-')
    await date_message(message=query.message, state=state_data, btn=msg_btn)


async def back_to_time(query: types.CallbackQuery, state: FSMContext):
    await state.update_data(start_time='-', stop_time='-')
    await time_messages(message=query.message, state=await state.get_data())


async def back_to_contact(query: types.CallbackQuery, state: FSMContext):
    await state.update_data(client='-')
    await contact_messages(message=query.message, state=await state.get_data())
