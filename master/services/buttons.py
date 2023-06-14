from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from master.services.callbacks import ServicesCallback
from master.services.strings import Btn

# MENU: "Menu service". BUTTONS: "Rename", "Delete", "Cost", "Time", "Back".
btn_menu_service = InlineKeyboardMarkup(row_width=2)
btn_menu_service.insert(InlineKeyboardButton(text=Btn.CHANGE_NAME, callback_data=ServicesCallback.CHANGE_NAME))
btn_menu_service.insert(InlineKeyboardButton(text=Btn.TIME, callback_data=ServicesCallback.CHANGE_TIME))
btn_menu_service.insert(InlineKeyboardButton(text=Btn.COST, callback_data=ServicesCallback.CHANGE_COST))
btn_menu_service.insert(InlineKeyboardButton(text=Btn.DELETE, callback_data=ServicesCallback.DELETE))
btn_menu_service.insert(InlineKeyboardButton(text=Btn.BACK, callback_data=ServicesCallback.BACK_SERVICES))

# MENU: "Delete service". BUTTONS: "Yes", "No".
btn_delete_service = InlineKeyboardMarkup(row_width=2)
btn_delete_service.insert(InlineKeyboardButton(text=Btn.YES, callback_data=ServicesCallback.DELETE_OK))
btn_delete_service.insert(InlineKeyboardButton(text=Btn.NO, callback_data=ServicesCallback.DELETE_CANCEL))

# MENU: "Add service". BUTTON: "OK".
btn_add_service = InlineKeyboardMarkup(row_width=2)
btn_add_service.insert(InlineKeyboardButton(text=Btn.YES, callback_data=ServicesCallback.ADD_SERVICE))


async def btn_categories(categories: list):
    btn = InlineKeyboardMarkup(row_width=2)
    for data in categories:
        btn.insert(InlineKeyboardButton(text=data[1], callback_data=f'{data[0]}{ServicesCallback.SERVICES_LIST}'))
    btn.row()
    return btn


async def btn_services(services: tuple):
    btn = InlineKeyboardMarkup(row_width=2)
    for data in services:
        btn.insert(InlineKeyboardButton(text=data[1], callback_data=f'{data[0]}{ServicesCallback.MENU}'))
    btn.row()
    btn.insert(InlineKeyboardButton(text=Btn.ADD, callback_data=ServicesCallback.ADD_NAME))
    btn.insert(InlineKeyboardButton(text=Btn.BACK, callback_data=ServicesCallback.BACK_CATEGORIES))
    return btn
