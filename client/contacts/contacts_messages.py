from aiogram import types
from aiogram.dispatcher import FSMContext

import bots
from client.add_register.parsers import format_contact, format_name
from client.contacts import buttons, db
from client.contacts.parsers import contact_msg_builder
from client.contacts.states import ContactsState
from client.contacts.strings import Title, Msg
from config import COUNTRY


async def contacts(message: types.Message):
    contacts_db = await db.get_contacts(client_id=message.chat.id)
    msg_text = f'<b>{Title.CONTACTS}</b>'
    msg_text = msg_text if len(contacts_db) != 0 else f'{msg_text}\n\n{Msg.NO_CONTACTS}'
    msg_btn = await buttons.contacts(clients_list=contacts_db)
    await message.answer(text=msg_text, reply_markup=msg_btn)


async def change_name(message: types.Message, state: FSMContext):
    name = await format_name(name=message.text)

    if name is not False:
        client_data = (await state.get_data()).get('client_data')
        if name != client_data[1]:
            await state.reset_state(with_data=False)
            client_data[1] = name
            await db.change_name(client_id=client_data[0], name=name)
            msg_text = f'<b>{Title.CONTACTS}</b>\n\n{await contact_msg_builder(contact_data=client_data)}'
            await bots.bot_client.edit_messages(
                message=message,
                text=msg_text,
                btn=buttons.contact_btn
            )
            await state.update_data(client_data=client_data)
        else:
            msg_text = f'<b>{Title.CONTACTS}</b>\n\n{Msg.ERROR_NAME}'
            await bots.bot_client.edit_messages(message=message, text=msg_text)
            await ContactsState.change_name.set()
    else:
        msg_text = f'<b>{Title.CONTACTS}</b>\n\n{Msg.ERROR_NAME}'
        await bots.bot_client.edit_messages(message=message, text=msg_text)
        await ContactsState.change_name.set()


async def change_contact(message: types.Message, state: FSMContext):
    contact = await format_contact(contact=message.text, country=COUNTRY)

    if contact is not False:
        client_data = (await state.get_data()).get('client_data')
        await db.change_contact(client_id=client_data[0], contact=contact)
        client_data[2] = contact
        msg_text = f'<b>{Title.CONTACTS}</b>\n\n{await contact_msg_builder(contact_data=client_data)}'
        await bots.bot_client.edit_messages(
            message=message,
            text=msg_text,
            btn=buttons.contact_btn
        )
        await state.update_data(client_data=client_data)
        await state.reset_state(with_data=False)
    else:
        msg_text = f'<b>{Title.CONTACTS}</b>\n\n{Msg.ERROR_CONTACT}'
        await bots.bot_client.edit_message_text(message=message, text=msg_text)
        await ContactsState.change_contact.set()
