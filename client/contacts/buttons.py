from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from client.contacts.callbacks import ContactsCallback
from client.contacts.strings import Btn


contact_btn = InlineKeyboardMarkup(row_width=2)
contact_btn.insert(InlineKeyboardButton(text=Btn.CHANGE_NAME, callback_data=ContactsCallback.CHANGE_NAME))
contact_btn.insert(InlineKeyboardButton(text=Btn.CHANGE_CONTACT, callback_data=ContactsCallback.CHANGE_CONTACT))
contact_btn.insert(InlineKeyboardButton(text=Btn.DELETE, callback_data=ContactsCallback.DELETE))
contact_btn.row()
contact_btn.insert(InlineKeyboardButton(text=Btn.BACK, callback_data=ContactsCallback.BACK_TO_CONTACTS))


delete_btn = InlineKeyboardMarkup(row_width=2)
delete_btn.insert(InlineKeyboardButton(text=Btn.DELETE, callback_data=ContactsCallback.DELETE_CONFIRM))
delete_btn.insert(InlineKeyboardButton(text=Btn.NO, callback_data=ContactsCallback.CANCEL))


async def contacts(clients_list: list) -> InlineKeyboardMarkup:
    btn = InlineKeyboardMarkup()
    for client in clients_list:
        btn.row()
        btn.insert(InlineKeyboardButton(
            text=client[1],
            callback_data=f"{client[0]}{ContactsCallback.ID}"
        ))
    return btn
