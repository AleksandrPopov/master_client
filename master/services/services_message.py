import time

from aiogram import types
from aiogram.dispatcher import FSMContext

from bots import bot_master
from master.services import db, buttons
from master.services.buttons import btn_menu_service
from master.services.parsers import msg_builder_add_service, msg_builder_menu_service
from master.services.state import ServicesState
from master.services.strings import Title, Msg
from master import parse


async def services(message: types.Message):
    categories_db = await db.get_categories(master_id=message.chat.id)
    msg_text = Title.SERVICES if len(categories_db) != 0 else f'{Title.SERVICES}{Msg.NOT_EXISTS_CATEGORIES}'
    msg_btn = await buttons.btn_categories(categories=categories_db)
    await message.answer(text=msg_text, reply_markup=msg_btn)


async def add_time(message: types.Message, state: FSMContext):
    service_name = await parse.format_name(name=message.text)
    category_name = (await state.get_data()).get('category_name')
    category_id = (await state.get_data()).get('category_id')

    if type(service_name) is str:
        result = await db.exists_service_name(
            master_id=message.chat.id,
            category_id=category_id,
            service_name=service_name
        )
        if result is False:
            msg_title = f'<b>{category_name}</b>\n\n'
            msg_text = f'{Msg.ENTER_TIME}\n{await msg_builder_add_service(service_name=service_name)}'

            await bot_master.edit_messages(message=message, text=f'{msg_title}{msg_text}')
            await state.update_data(service_name=service_name)
            await ServicesState.add_time.set()
        else:
            msg_title = f'<b>{category_name}</b>\n\n'
            msg_text = f'{Msg.EXISTS_SERVICES}\n{await msg_builder_add_service()}'

            await bot_master.edit_messages(message=message, text=f'{msg_title}{msg_text}')
            await ServicesState.add_name.set()
    else:
        msg_title = f'<b>{category_name}</b>\n\n'
        msg_text = f'{Msg.ERROR_NAME}\n{await msg_builder_add_service()}'

        await bot_master.edit_messages(message=message, text=f'{msg_title}{msg_text}')
        await ServicesState.add_name.set()


async def add_cost(message: types.Message, state: FSMContext):
    category_name = (await state.get_data()).get('category_name')
    service_name = (await state.get_data()).get('service_name')
    service_time = message.text

    if service_time.isdigit() and len(service_time) < 5:
        msg_title = f'<b>{category_name}</b>\n\n'
        msg_text = f'{Msg.ENTER_COST}\n{await msg_builder_add_service(service_name=service_name, service_time=str(service_time))}'

        await bot_master.edit_messages(message=message, text=f'{msg_title}{msg_text}')
        await state.update_data(service_time=time.strftime('%H:%M:%S', time.gmtime(int(service_time) * 60)))
        await ServicesState.add_cost.set()
    else:
        msg_title = f'<b>{category_name}</b>\n\n'
        msg_text = f'{Msg.ERROR_TIME}\n{await msg_builder_add_service(service_name=service_name)}'

        await bot_master.edit_messages(message=message, text=f'{msg_title}{msg_text}')
        await ServicesState.add_time.set()


async def add_service(message: types.Message, state: FSMContext):
    await state.reset_state(with_data=False)
    category_id = (await state.get_data()).get('category_id')
    category_name = (await state.get_data()).get('category_name')
    service_name = (await state.get_data()).get('service_name')
    service_time = (await state.get_data()).get('service_time')
    service_cost = message.text

    if service_cost.isdigit() and len(service_cost) < 4:
        service_id = await db.add_service(
            master_id=message.chat.id,
            category_id=category_id,
            service_name=service_name,
            service_time=service_time,
            service_cost=service_cost
        )
        msg_text = f'{await msg_builder_menu_service(service_id=service_id, category_name=category_name)}'

        await bot_master.edit_messages(message=message, text=msg_text, btn=btn_menu_service)
        await state.update_data(service_id=service_id)
    else:
        msg_title = f'<b>{category_name}</b>\n\n{Msg.ERROR_COST}\n'
        msg_text = f'{await msg_builder_add_service(service_name=service_name, service_time=str(service_time))}'

        await bot_master.edit_messages(message=message, text=f'{msg_title}{msg_text}')
        await ServicesState.add_cost.set()


async def change_name(message: types.Message, state: FSMContext):
    service_name = await parse.format_name(name=message.text)
    category_name = (await state.get_data()).get('category_name')
    service_current_name = (await state.get_data()).get('service_name')
    service_id = (await state.get_data()).get('service_id')

    if service_name is not False:
        if service_name != service_current_name:
            await db.change_name_service(service_id=service_id, service_name=service_name)
            msg_text = f'{await msg_builder_menu_service(service_id=service_id, category_name=category_name)}'

            await bot_master.edit_messages(message=message, text=msg_text, btn=buttons.btn_menu_service)
            await state.update_data(service_name=service_name)
            await state.reset_state(with_data=False)
        else:
            msg_text = f'<b>{service_current_name}</b>\n\n{Msg.EXISTS_SERVICES}'

            await bot_master.edit_messages(message=message, text=msg_text)
            await ServicesState.change_name.set()
    else:
        msg_text = f'<b>{category_name}</b>\n\n{Msg.ERROR_NAME}'

        await bot_master.edit_messages(message=message, text=msg_text)
        await ServicesState.change_name.set()


async def change_time(message: types.Message, state: FSMContext):
    service_time = message.text
    category_name = (await state.get_data()).get('category_name')
    service_name = (await state.get_data()).get('service_name')
    service_id = (await state.get_data()).get('service_id')

    if service_time.isdigit() and len(service_time) < 4:
        service_time = time.strftime('%H:%M:%S', time.gmtime(int(service_time) * 60))
        await db.change_time_service(service_id=service_id, time=service_time)
        msg_text = f'{await msg_builder_menu_service(service_id=service_id, category_name=category_name)}'

        await bot_master.edit_messages(message=message, text=msg_text, btn=buttons.btn_menu_service)
        await state.reset_state(with_data=False)
    else:
        msg_text = f'<b>{service_name}</b>\n\n{Msg.ERROR_TIME}'

        await bot_master.edit_messages(message=message, text=msg_text)
        await ServicesState.change_time.set()


async def change_cost(message: types.Message, state: FSMContext):
    service_cost = message.text
    category_name = (await state.get_data()).get('category_name')
    service_name = (await state.get_data()).get('service_name')
    service_id = (await state.get_data()).get('service_id')

    if service_cost.isdigit() and len(service_cost) < 5:
        await db.change_cost_service(service_id=service_id, cost=service_cost)
        msg_text = f'{await msg_builder_menu_service(service_id=service_id, category_name=category_name)}'

        await bot_master.edit_messages(message=message, text=msg_text, btn=buttons.btn_menu_service)
        await state.reset_state(with_data=False)
    else:
        msg_text = f'<b>{service_name}</b>\n\n{Msg.ERROR_COST}'

        await bot_master.edit_messages(message=message, text=msg_text)
        await ServicesState.change_cost.set()
