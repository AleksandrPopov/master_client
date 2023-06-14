from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from master.categories.callbacks import CategoriesCallback
from master.categories.strings import Btn

# MENU: "Menu category". BUTTONS: "Rename", "Delete", "Back".
btn_menu_category = InlineKeyboardMarkup(row_width=2)
btn_menu_category.insert(
    InlineKeyboardButton(text=Btn.CHANGE_NAME, callback_data=CategoriesCallback.CHANGE))
btn_menu_category.insert(InlineKeyboardButton(text=Btn.DELETE, callback_data=CategoriesCallback.DELETE))
btn_menu_category.row()
btn_menu_category.insert(InlineKeyboardButton(text=Btn.BACK, callback_data=CategoriesCallback.BACK))

# MENU: "Delete category". BUTTONS: "Yes", "No".
btn_delete_category = InlineKeyboardMarkup(row_width=2)
btn_delete_category.insert(InlineKeyboardButton(text=Btn.YES, callback_data=CategoriesCallback.DELETE_OK))
btn_delete_category.insert(InlineKeyboardButton(text=Btn.NO, callback_data=CategoriesCallback.DELETE_CANCEL))


# MENU: "Categories". BUTTONS: "*categories", "Add".
async def btn_categories(categories: tuple):
    btn = InlineKeyboardMarkup(row_width=2)
    for data in categories:
        btn.insert(InlineKeyboardButton(text=data[1], callback_data=f'{data[0]}{CategoriesCallback.MENU}'))
    btn.row()
    btn.insert(InlineKeyboardButton(text=Btn.ADD, callback_data=CategoriesCallback.ADD))
    return btn
