from aiogram import types
from aiogram.dispatcher import FSMContext

from master.services import db, buttons
from master.services.buttons import btn_services, btn_menu_service
from master.services.callbacks import ServicesCallback
from master.services.state import ServicesState
from master.services.strings import Msg, Title
from master.services.parsers import msg_builder_add_service, msg_builder_menu_service


async def services(query: types.CallbackQuery, state: FSMContext):
    category_id = int(query.data.rstrip(ServicesCallback.SERVICES_LIST))
    category_name = await db.get_category(category_id=category_id)
    services_db = await db.get_services(category_id=category_id)
    msg_text = f'<b>{category_name}</b>\n\n'
    msg_text = msg_text if len(services_db) != 0 else f'{msg_text}{Msg.NOT_EXISTS_SERVICES}'
    msg_btn = await buttons.btn_services(services=services_db)

    await query.message.edit_text(text=msg_text, reply_markup=msg_btn)
    await state.update_data(category_id=category_id, category_name=category_name)


async def add_name(query: types.CallbackQuery, state: FSMContext):
    category_name = (await state.get_data()).get('category_name')
    msg_title = f'<b>{category_name}</b>\n\n'
    msg_text = f'{Msg.ENTER_SERVICE_NAME}\n{await msg_builder_add_service()}'

    await query.message.edit_text(text=f'{msg_title}{msg_text}')
    await ServicesState.add_name.set()


async def add_service(query: types.CallbackQuery, state: FSMContext):
    category_name = (await state.get_data()).get('category_name')
    category_id = (await state.get_data()).get('category_id')
    services_db = await db.get_services(category_id=category_id)
    msg_text = f'<b>{category_name}</b>'
    msg_btn = await btn_services(services=services_db)

    await query.message.edit_text(text=msg_text, reply_markup=msg_btn)


async def menu(query: types.CallbackQuery, state: FSMContext):
    service_id = int(query.data.rstrip(ServicesCallback.MENU))
    category_name = (await state.get_data()).get('category_name')
    service_name = (await db.get_service(service_id=service_id))[0]

    msg_text = f'{await msg_builder_menu_service(service_id=service_id, category_name=category_name)}'

    await query.message.edit_text(text=msg_text, reply_markup=btn_menu_service)
    await state.update_data(service_id=service_id, service_name=service_name)


async def change_name(query: types.CallbackQuery, state: FSMContext):
    service_name = (await state.get_data()).get('service_name')
    msg_text = f'<b>{service_name}</b>\n\n{Msg.ENTER_NAME}'

    await query.message.edit_text(text=msg_text)
    await ServicesState.change_name.set()


async def change_time(query: types.CallbackQuery, state: FSMContext):
    service_name = (await state.get_data()).get('service_name')
    msg_text = f'<b>{service_name}</b>\n\n{Msg.ENTER_TIME}'

    await query.message.edit_text(text=msg_text)
    await ServicesState.change_time.set()


async def change_cost(query: types.CallbackQuery, state: FSMContext):
    service_name = (await state.get_data()).get('service_name')
    msg_text = f'<b>{service_name}</b>\n\n{Msg.ENTER_COST}'

    await query.message.edit_text(text=msg_text)
    await ServicesState.change_cost.set()


async def back_to_categories(query: types.CallbackQuery):
    categories_db = await db.get_categories(master_id=query.message.chat.id)
    msg_text = Title.SERVICES if len(categories_db) != 0 else f'{Title.SERVICES}{Msg.NOT_EXISTS_CATEGORIES}'
    msg_btn = await buttons.btn_categories(categories=categories_db)

    await query.message.edit_text(text=msg_text, reply_markup=msg_btn)


async def back_to_services(query: types.CallbackQuery, state: FSMContext):
    category_id = (await state.get_data()).get('category_id')
    category_name = (await state.get_data()).get('category_name')
    services_db = await db.get_services(category_id=category_id)
    msg_text = f'<b>{category_name}</b>\n\n'
    msg_text = msg_text if len(services_db) != 0 else f'{msg_text}{Msg.NOT_EXISTS_SERVICES}'
    msg_btn = await buttons.btn_services(services=services_db)

    await query.message.edit_text(text=msg_text, reply_markup=msg_btn)


async def delete_service(query: types.CallbackQuery, state: FSMContext):
    service_name = (await state.get_data()).get('service_name')
    msg_text = f'<b>{service_name}</b>\n\n{Msg.DELETE}'

    await query.message.edit_text(text=msg_text, reply_markup=buttons.btn_delete_service)


async def delete_cancel(query: types.CallbackQuery, state: FSMContext):
    category_name = (await state.get_data()).get('category_name')
    service_id = (await state.get_data()).get('service_id')
    msg_text = f'{await msg_builder_menu_service(service_id=service_id, category_name=category_name)}'

    await query.message.edit_text(text=msg_text, reply_markup=buttons.btn_menu_service)


async def delete_ok(query: types.CallbackQuery, state: FSMContext):
    category_id = (await state.get_data()).get('category_id')
    category_name = (await state.get_data()).get('category_name')
    service_id = (await state.get_data()).get('service_id')
    await db.delete_service(service_id=service_id)
    services_db = await db.get_services(category_id=category_id)
    msg_text = f'<b>{category_name}</b>\n\n'
    msg_text = msg_text if len(services_db) != 0 else f'{msg_text}{Msg.NOT_EXISTS_SERVICES}'
    msg_btn = await buttons.btn_services(services=services_db)

    await query.message.edit_text(text=msg_text, reply_markup=msg_btn)
