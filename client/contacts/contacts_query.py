from aiogram import types
from aiogram.dispatcher import FSMContext

from client.contacts import buttons, db
from client.contacts.callbacks import ContactsCallback
from client.contacts.parsers import contact_msg_builder
from client.contacts.states import ContactsState
from client.contacts.strings import Title, Msg


async def select_contact(query: types.CallbackQuery, state: FSMContext):
    client_id = int(query.data.rstrip(ContactsCallback.ID))
    contact = await db.get_contact(client_id=client_id)
    msg_text = f'<b>{Title.CONTACTS}</b>\n\n{await contact_msg_builder(contact_data=contact)}'
    msg_btn = buttons.contact_btn

    await state.update_data(client_data=list(contact))
    await query.message.edit_text(text=msg_text, reply_markup=msg_btn)


async def change_name(query: types.CallbackQuery):
    msg_text = f'<b>{Title.CONTACTS}</b>\n\n{Msg.ENTER_NEW_NAME}'
    await query.message.edit_text(text=msg_text)
    await ContactsState.change_name.set()


async def change_contact(query: types.CallbackQuery):
    msg_text = f'<b>{Title.CONTACTS}</b>\n\n{Msg.ENTER_NEW_CONTACT}'
    await query.message.edit_text(text=msg_text)
    await ContactsState.change_contact.set()


async def back_to_contacts(query: types.CallbackQuery, state: FSMContext):
    await state.finish()
    msg_text = f'<b>{Title.CONTACTS}</b>'
    contacts_db = await db.get_contacts(client_id=query.message.chat.id)
    msg_text = msg_text if len(contacts_db) != 0 else f'{msg_text}\n\n{Msg.NO_CONTACTS}'
    msg_btn = await buttons.contacts(clients_list=contacts_db)
    await query.message.edit_text(text=msg_text, reply_markup=msg_btn)


async def delete_contact(query: types.CallbackQuery):
    msg_text = f'<b>{Title.CONTACTS}</b>\n\n{Msg.DELETE}'
    msg_btn = buttons.delete_btn
    await query.message.edit_text(text=msg_text, reply_markup=msg_btn)


async def cancel_delete_contact(query: types.CallbackQuery, state: FSMContext):
    client_data = (await state.get_data()).get('client_data')
    msg_text = f'<b>{Title.CONTACTS}</b>\n\n{await contact_msg_builder(contact_data=client_data)}'
    msg_btn = buttons.contact_btn
    await query.message.edit_text(text=msg_text, reply_markup=msg_btn)


async def delete_confirm(query: types.CallbackQuery, state: FSMContext):
    client_id = int((await state.get_data()).get('client_data')[0])
    registers = await db.get_client_registers(client_id=client_id)
    if registers is not True:
        await db.delete_contact(client_id=client_id)
        contacts_db = await db.get_contacts(client_id=query.message.chat.id)
        msg_text = f'<b>{Title.CONTACTS}</b>\n\n{await contact_msg_builder() if len(contacts_db) else Msg.NO_CONTACTS}'
        msg_btn = await buttons.contacts(clients_list=contacts_db)
        await query.message.edit_text(text=msg_text, reply_markup=msg_btn)
        await state.finish()
    else:
        await query.answer(text=Msg.EXISTS_REGISTERS, show_alert=True)
