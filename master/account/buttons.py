from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup

from master.account.callbacks import AccountCallback
from master.account.strings import Btn

btn_get_contact = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
btn_get_contact.insert(KeyboardButton(text=Btn.GET_CONTACT, request_contact=True))

account_menu = InlineKeyboardMarkup(row_width=2)
account_menu.insert(InlineKeyboardButton(text=Btn.CHANGE_NAME, callback_data=AccountCallback.CHANGE_NAME))
account_menu.insert(InlineKeyboardButton(text=Btn.CHANGE_CONTACT, callback_data=AccountCallback.CHANGE_CONTACT))
account_menu.insert(InlineKeyboardButton(text=Btn.DELETE_ACCOUNT, callback_data=AccountCallback.DELETE_ACCOUNT))

btn_delete_confirm = InlineKeyboardMarkup(row_width=2)
btn_delete_confirm.insert(InlineKeyboardButton(text=Btn.YES, callback_data=AccountCallback.DELETE_CONFIRM))
btn_delete_confirm.insert(InlineKeyboardButton(text=Btn.NO, callback_data=AccountCallback.DELETE_CANCEL))
