import asyncio
import logging

from aiohttp import web

from client.add_register.add_register_handlers import register_add_register_handlers
from client.contacts.contacts_handlers import register_contacts_handlers
from client.filter_handler import register_filter_handler
from client.registers.registers_handlers import register_registers_handlers
from config import HOST, CERT, PORT, PORT_CLIENT, NAME, PORT_MASTER
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from aiogram.dispatcher.webhook import get_new_configured_app

from bots import bot_client, commands_client, dp_client, bot_master, dp_master, commands_master
from database.connector import engine
from database.tables import create
from master.account.account_handlers import register_account_handlers
from master.categories.categories_handlers import register_categories_handlers
from master.days_off.days_off_handlers import register_days_off_handlers
from master.schedules.schedules_handlers import register_schedules_handlers
from master.services.services_handlers import register_services_handlers
from scheduler.run_schedulers import run

logging.basicConfig(level=logging.DEBUG)
dp_client.middleware.setup(LoggingMiddleware())


async def on_startup_client(app):
    await bot_client.set_webhook(f'https://{HOST}:{PORT}/root/bots/master/client/', certificate=open(CERT, 'rb'))
    await commands_client()
    await register_add_register_handlers(dp_client)
    await register_registers_handlers(dp_client)
    await register_contacts_handlers(dp_client)
    await register_filter_handler(dp_client)
    create(engine=engine)
    await commands_master()
    await register_schedules_handlers(dp=dp_master)
    await register_days_off_handlers(dp=dp_master)
    await register_categories_handlers(dp=dp_master)
    await register_services_handlers(dp=dp_master)
    await register_account_handlers(dp=dp_master)
    await register_registers_handlers(dp=dp_master)
    await register_filter_handler(dp=dp_master)
    asyncio.create_task(run())


async def on_shutdown_client(app):
    logging.warning('Shutting down..')
    await bot_client.delete_webhook()
    await dp_client.storage.close()
    await dp_client.storage.wait_closed()
    await bot_master.delete_webhook()
    await dp_master.storage.close()
    await dp_master.storage.wait_closed()
    logging.warning('Bye!')


if __name__ == '__main__':
    client = web
    master = web
    app_client = get_new_configured_app(dispatcher=dp_client, path=f'/root/bots/master/client/')
    app_client.on_startup.append(on_startup_client)
    app_client.on_shutdown.append(on_shutdown_client)

    app_master = get_new_configured_app(dispatcher=dp_master, path=f'/root/bots/master/master/')
    app_master.on_startup.append(on_startup_client)
    app_master.on_shutdown.append(on_shutdown_client)

    client.run_app(app_client, host=f'0.0.0.0', port=PORT_CLIENT)
    master.run_app(app_client, host=f'0.0.0.0', port=PORT_MASTER)
