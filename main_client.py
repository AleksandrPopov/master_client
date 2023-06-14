import logging

from aiohttp import web

from client.add_register.add_register_handlers import register_add_register_handlers
from client.contacts.contacts_handlers import register_contacts_handlers
from client.registers.registers_handlers import register_registers_handlers
from config import HOST, CERT, PORT, PORT_CLIENT, NAME
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from aiogram.dispatcher.webhook import get_new_configured_app

from bots import bot_client, commands_client, dp_client

logging.basicConfig(level=logging.DEBUG)
dp_client.middleware.setup(LoggingMiddleware())


async def on_startup_client(app):
    await bot_client.set_webhook(f'{HOST}:{PORT}/{NAME}-client/', certificate=open(CERT, 'rb'))
    await commands_client()
    await register_add_register_handlers(dp_client)
    await register_registers_handlers(dp_client)
    await register_contacts_handlers(dp_client)


async def on_shutdown_client(app):
    logging.warning('Shutting down..')
    await bot_client.delete_webhook()
    await dp_client.storage.close()
    await dp_client.storage.wait_closed()
    logging.warning('Bye!')


if __name__ == '__main__':
    app_client = get_new_configured_app(dispatcher=dp_client, path=f'/{NAME}-client/')
    app_client.on_startup.append(on_startup_client)
    app_client.on_shutdown.append(on_shutdown_client)

    web.run_app(app_client, host=f'{NAME}-client', port=PORT_CLIENT)
