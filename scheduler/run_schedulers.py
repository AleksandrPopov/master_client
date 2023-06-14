import asyncio
import aioschedule
from scheduler.schedulers import register_incoming, delete_register


async def run():
    aioschedule.every(60).seconds.do(register_incoming)
    aioschedule.every(60).seconds.do(delete_register)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(5)
