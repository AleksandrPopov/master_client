import datetime

from country_currencies import get_by_country
from config import COUNTRY
from master.services import db

from master.services.strings import Msg


async def msg_builder_add_service(service_name: str = '-', service_time: str = '-', cost: str = '-') -> str:
    service_time = await _time_parser(time=service_time)
    return await _msg_builder(name=service_name, time=service_time, cost=cost)


async def msg_builder_menu_service(service_id: int, category_name: str) -> str:
    service_db = await db.get_service(service_id=service_id)
    name, time, cost = service_db[0], service_db[1], service_db[2]

    time = await _time_parser(time=time)
    cost = f'{cost} {get_by_country(COUNTRY)[0]}'

    msg_title = f'<b>{category_name}</b>\n\n'
    msg_text = f'{await _msg_builder(name=name, time=time, cost=cost)}'

    return f'{msg_title}{msg_text}'


async def _time_parser(time: str = '-') -> str:
    if time != '-':
        if type(time) is str and time.isdigit():
            time = str(datetime.timedelta(minutes=int(time)))
        if type(time) is str and not time.isdigit():
            time = datetime.datetime.strptime(time, '%H:%M:%S')

        if time.hour != 0 and time.minute != 0:
            time = f"{time.hour} {Msg.HOUR} {time.minute} {Msg.MINUTES}"
        elif time.hour != 0 and time.minute == 0:
            time = f"{time.hour} {Msg.HOUR}"
        else:
            time = f"{time.minute} {Msg.MINUTES}"

    return time


async def _msg_builder(name: str, time: str, cost: str) -> str:
    len_max = max([len(Msg.NAME), len(Msg.TIME), len(Msg.COST)])

    name_len = " " * (len_max - len(Msg.NAME) + 3)
    time_len = " " * (len_max - len(Msg.TIME) + 3)
    cost_len = " " * (len_max - len(Msg.COST) + 3)

    return f"<code>{Msg.NAME}:{name_len}</code>{name}\n" \
           f"<code>{Msg.TIME}:{time_len}</code>{time}\n" \
           f"<code>{Msg.COST}:{cost_len}</code>{cost}\n"
