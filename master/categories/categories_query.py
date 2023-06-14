from aiogram import types
from aiogram.dispatcher import FSMContext

from master.categories import db, buttons
from master.categories.strings import Title, Msg
from master.categories.state import CategoriesState
from master.categories.callbacks import CategoriesCallback


async def add_category(query: types.CallbackQuery):
    msg_text = f'{Title.CATEGORIES}{Msg.ENTER_CATEGORY_NAME}'
    await query.message.edit_text(text=msg_text)
    await CategoriesState.add_category.set()


async def menu_category(query: types.CallbackQuery, state: FSMContext):
    category_id = int(query.data.rstrip(CategoriesCallback.MENU))
    category_name = await db.get_category(category_id=category_id)
    msg_text = f'<b>{category_name}</b>'
    await query.message.edit_text(text=msg_text, reply_markup=buttons.btn_menu_category)
    await state.update_data(category_id=category_id, category_name=category_name)


async def change_name_category(query: types.CallbackQuery, state: FSMContext):
    category_name = (await state.get_data()).get("category_name")
    msg_text = f'<b>{category_name}</b>\n\n{Msg.ENTER_CATEGORY_NAME}'
    await query.message.edit_text(text=msg_text)
    await CategoriesState.change_name.set()


async def question_delete_category(query: types.CallbackQuery, state: FSMContext):
    category_name = (await state.get_data()).get('category_name')
    msg_text = f'<b>{category_name}\n\n</b>{Msg.DELETE}'
    await query.message.edit_text(text=msg_text, reply_markup=buttons.btn_delete_category)


async def back_menu_category(query: types.CallbackQuery, state: FSMContext):
    category_name = (await state.get_data()).get('category_name')
    msg_text = f'<b>{category_name}\n\n</b>'
    await query.message.edit_text(text=msg_text, reply_markup=buttons.btn_menu_category)


async def delete_category(query: types.CallbackQuery, state: FSMContext):
    category_id = (await state.get_data()).get('category_id')
    await db.delete_category(category_id=category_id)
    categories_db = await db.get_categories(master_id=query.message.chat.id)
    msg_text = Title.CATEGORIES if len(categories_db) != 0 else f'{Title.CATEGORIES}{Msg.ADD_CATEGORIES}'
    await query.message.edit_text(text=msg_text, reply_markup=await buttons.btn_categories(categories=categories_db))
    await state.finish()


async def back_to_categories(query: types.CallbackQuery, state: FSMContext):
    await state.finish()
    categories_db = await db.get_categories(master_id=query.message.chat.id)
    msg_text = Title.CATEGORIES if len(categories_db) != 0 else f'{Title.CATEGORIES}{Msg.ADD_CATEGORIES}'
    await query.message.edit_text(text=msg_text, reply_markup=await buttons.btn_categories(categories=categories_db))
