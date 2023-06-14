from aiogram import types
from aiogram.dispatcher import FSMContext

import bots
from config import COUNTRY

from client.add_register import buttons, db
from client.add_register.db import get_masters
from client.add_register.parsers import add_register_msg_builder, time_exists, format_contact, format_name
from client.add_register.states import AddRegisterState
from client.add_register.strings import Title, Msg


async def start(message: types.Message, state: FSMContext):
    masters_list = await get_masters()
    is_client = await db.get_client_exists(client_id=message.chat.id)
    await state.update_data(categories=[], services=[])

    if is_client:
        if len(masters_list) == 1:
            await state.update_data(master=list(masters_list[0]), start='categories')
            categories_db = await db.get_categories(master_id=masters_list[0][0])

            msg_text = f"<b>{Title.CHECK_CATEGORY}</b>\n\n{await add_register_msg_builder(state=await state.get_data())}"
            msg_btn = await buttons.categories(categories_db=categories_db)
            await message.answer(text=msg_text, reply_markup=msg_btn)

        if len(masters_list) > 1:
            await state.update_data(client_id=message.chat.id, start='masters')

            msg_text = f"<b>{Title.CHECK_MASTER}</b>\n\n{await add_register_msg_builder(state=await state.get_data())}"
            msg_btn = await buttons.masters(masters_list=masters_list)

            await message.answer(text=msg_text, reply_markup=msg_btn)

        if len(masters_list) == 0:
            await message.answer(text=f"<b>{Title.NO_ADMINS}</b>")
    else:
        await message.answer(text=Msg.GET_CONTACT, reply_markup=buttons.btn_get_contact)


async def categories_message(message: types.Message, state: dict, categories_db: list, back: str = None):
    msg_text = f"<b>{Title.CHECK_CATEGORY}</b>\n\n{await add_register_msg_builder(state=state)}"
    msg_btn = await buttons.categories(back=back, categories_db=categories_db)
    await message.edit_text(text=msg_text, reply_markup=msg_btn)


async def services_message(message: types.Message, state: dict, services_db: list):
    msg_text = f"<b>{Title.CHECK_SERVICE}</b>\n\n{await add_register_msg_builder(state=state)}"
    msg_btn = await buttons.services(services_db=services_db)
    await message.edit_text(text=msg_text, reply_markup=msg_btn)


async def more_services_messages(message: types.Message, state: dict):
    msg_text = f"<b>{Title.CHECK_MORE}</b>\n\n{await add_register_msg_builder(state=state)}"
    msg_btn = await buttons.more_services()
    await message.edit_text(text=msg_text, reply_markup=msg_btn)


async def date_message(message: types.Message, state: dict, btn):
    msg_text = f"<b>{Title.CHECK_DATE}</b>\n\n{await add_register_msg_builder(state=state)}"
    await message.edit_text(text=msg_text, reply_markup=btn)


async def time_messages(message: types.Message, state: dict):
    msg_text = f"<b>{Title.CHECK_TIME}</b>\n\n{await add_register_msg_builder(state=state)}"
    msg_btn = await buttons.time(time_list=await time_exists(state=state))
    await message.edit_text(text=msg_text, reply_markup=msg_btn)


async def contact_messages(message: types.Message, state: dict):
    clients_list = await db.get_clients(client_id=message.chat.id)
    msg_text = f"<b>{Title.CHECK_CONTACT}</b>\n\n{await add_register_msg_builder(state=state)}"
    msg_btn = await buttons.contacts(clients_list=clients_list)
    await message.edit_text(text=msg_text, reply_markup=msg_btn)


async def add_contact(message: types.Message, state: FSMContext):
    contact = await format_contact(contact=message.contact.phone_number, country=COUNTRY)
    name = await format_name(name=message.from_user.first_name)
    await db.add_client(
        client_id=message.chat.id,
        client_name=name if name is not False else 'Client',
        client_contact=contact
    )
    await start(message=message, state=state)


async def add_contact_name(message: types.Message, state: FSMContext):
    name = await format_name(name=message.text)

    if type(name) is str:
        msg_text = f'<b>{Title.CONTACTS}</b>\n\n{Msg.SET_CONTACT}'
        await bots.bot_client.edit_messages(message=message, text=msg_text)
        await state.update_data(client_name=name)
        await AddRegisterState.add_contact_number.set()
    else:
        msg_text = f'<b>{Title.CONTACTS}</b>\n\n{Msg.ERROR_NAME}'
        await bots.bot_client.edit_messages(message=message, text=msg_text)
        await AddRegisterState.add_contact_name.set()


async def add_contact_number(message: types.Message, state: FSMContext):
    contact = await format_contact(contact=message.text, country=COUNTRY)

    if contact is not False:
        name = (await state.get_data()).get('client_name')
        await db.add_client(client_id=message.chat.id, client_name=name, client_contact=contact)
        clients_list = await db.get_clients(client_id=message.chat.id)
        msg_text = f"<b>{Title.CHECK_CONTACT}</b>\n\n{await add_register_msg_builder(state=await state.get_data())}"
        msg_btn = await buttons.contacts(clients_list=clients_list)
        await state.reset_state(with_data=False)
        await bots.bot_client.edit_messages(message=message, text=msg_text, btn=msg_btn)
    else:
        msg_text = f'<b>{Title.CONTACTS}</b>\n\n{Msg.ERROR_CONTACT}'
        await bots.bot_client.edit_messages(message=message, text=msg_text)
        await AddRegisterState.add_contact_number.set()
