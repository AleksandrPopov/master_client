import asyncio
import logging

from aiohttp import web

from bots import dp_master, bot_master, commands_master
from config import HOST, PORT_MASTER, CERT, PORT, NAME
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from database.connector import engine
from database.tables import create
from master.categories.categories_handlers import register_categories_handlers
from master.filter_handler import register_filter_handler
from master.registers.registers_handlers import register_registers_handlers
from aiogram.dispatcher.webhook import get_new_configured_app
from master.schedules.schedules_handlers import register_schedules_handlers
from master.days_off.days_off_handlers import register_days_off_handlers
from master.account.account_handlers import register_account_handlers
from master.services.services_handlers import register_services_handlers
from scheduler.run_schedulers import run

logging.basicConfig(level=logging.DEBUG)
dp_master.middleware.setup(LoggingMiddleware())


async def on_startup_master(app):
    await bot_master.set_webhook(f'https://{HOST}:{PORT}/root/bots/master/master/', certificate=open(CERT, 'rb'))
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


async def on_shutdown_master(app):
    logging.warning('Shutting down..')
    await bot_master.delete_webhook()
    await dp_master.storage.close()
    await dp_master.storage.wait_closed()
    logging.warning('Bye!')


if __name__ == '__main__':
    app_master = get_new_configured_app(dispatcher=dp_master, path=f'/root/bots/master/master/')
    app_master.on_startup.append(on_startup_master)
    app_master.on_shutdown.append(on_shutdown_master)
    web.run_app(app_master, host=f'0.0.0.0', port=PORT_MASTER)
