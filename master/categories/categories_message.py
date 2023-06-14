from aiogram import types
from aiogram.dispatcher import FSMContext

from bots import bot_master
from master import parse

from master.categories import db, buttons
from master.categories.strings import Title, Msg
from master.categories.state import CategoriesState


async def categories(message: types.Message):
    categories_db = await db.get_categories(master_id=message.chat.id)
    msg_text = Title.CATEGORIES if len(categories_db) != 0 else f'{Title.CATEGORIES}{Msg.ADD_CATEGORIES}'
    await message.answer(text=msg_text, reply_markup=await buttons.btn_categories(categories=categories_db))


async def add_category(message: types.Message, state: FSMContext):
    category_name = await parse.format_name(name=message.text)

    if category_name is not False:
        result = await db.add_category(master_id=message.chat.id, category_mame=category_name)

        if result:
            await state.finish()
            categories_db = await db.get_categories(master_id=message.chat.id)
            msg_text = Title.CATEGORIES if len(categories_db) != 0 else f'{Title.CATEGORIES}{Msg.ADD_CATEGORIES}'
            msg_btn = await buttons.btn_categories(categories=categories_db)
            await bot_master.edit_messages(message=message, text=msg_text, btn=msg_btn)

        else:
            msg_text = f'{Title.CATEGORIES}{Msg.ERROR_EXISTS_NAME}'
            await bot_master.edit_messages(message=message, text=msg_text)
            await CategoriesState.add_category.set()
    else:
        msg_text = f'{Title.CATEGORIES}{Msg.ERROR_LONG_NAME}'
        await bot_master.edit_messages(message=message, text=msg_text)
        await CategoriesState.add_category.set()


async def change_name(message: types.Message, state: FSMContext):
    category_new_name = await parse.format_name(name=message.text)
    category_id = (await state.get_data()).get('category_id')
    category_name = (await state.get_data()).get('category_name')

    if category_new_name is not False:
        if category_name != category_new_name:
            await db.change_category_name(category_id=category_id, category_name=category_new_name)
            await state.reset_state(with_data=False)
            msg_text = f'<b>{category_new_name}</b>'
            await bot_master.edit_messages(message=message, text=msg_text, btn=buttons.btn_menu_category)
            await state.update_data(category_name=category_new_name)
        else:
            msg_text = f'<b>{category_name}</b>\n\n{Msg.ERROR_EXISTS_NAME}'
            await bot_master.edit_messages(message=message, text=msg_text)
            await CategoriesState.change_name.set()
    else:
        msg_text = f'<b>{category_name}</b>\n\n{Msg.ERROR_LONG_NAME}'
        await bot_master.edit_messages(message=message, text=msg_text)
        await CategoriesState.change_name.set()
