import calendar
from datetime import datetime, timedelta

from country_currencies import get_by_country

from config import COUNTRY
from master.registers import db
from master.registers.strings import Msg, Title


async def exists_date(master_id: int, date: datetime.date) -> list:
    month_calendar = calendar.monthcalendar(year=date.year, month=date.month)
    registers_db = await db.get_registers_date(master_id=master_id, month=date.month, year=date.year)
    month_calendar = await _days_list(calendar_list=month_calendar, registers=registers_db)

    return month_calendar


async def _days_list(calendar_list: list, registers: list) -> list:
    days_registers = []
    days = []
    for date in registers:
        days_registers.append(date.day)

    for week in calendar_list:
        for i, calendar_day in enumerate(week):
            if calendar_day not in days_registers:
                days.append(0)
            else:
                days.append(calendar_day)
    return days


async def registers_time(registers_times: list, master_id: int, date: datetime.date) -> list:
    schedule = await db.get_schedule(master_id=master_id, day=date.weekday())
    last_register = registers_times[0][-1]
    time_list = []

    start_time = datetime.combine(date.min, schedule[0][0])
    stop_time = datetime.combine(date.min, schedule[0][1])
    if last_register > stop_time.time():
        stop_time = stop_time.combine(date=stop_time.date(), time=last_register) + timedelta(minutes=30)
    while start_time < stop_time:
        if any(i[1] == start_time.time() for i in registers_times):
            for register in registers_times:
                if register[1] == start_time.time():
                    time_list.append({'id': int(register[0]), 'time': start_time.time()})
        else:
            time_list.append({'id': 0, 'time': start_time.time().min})
        start_time += timedelta(minutes=30)

    if len(time_list) % 3 == 1:
        time_list.append({'id': 0, 'time': start_time.time().min})
        time_list.append({'id': 0, 'time': start_time.time().min})

    if len(time_list) % 3 == 2:
        time_list.append({'id': 0, 'time': start_time.time().min})

    return time_list


async def register_msg_builder(register: dict) -> str:
    len_max = max(
        [len(Msg.CATEGORY),
         len(Msg.SERVICE),
         len(Msg.DATE),
         len(Msg.TIME),
         len(Msg.CONTACT),
         len(Msg.NAME),
         len(Msg.COST)])

    len_category = " " * (len_max - len(Msg.CATEGORY) + 3)
    len_service = " " * (len_max - len(Msg.SERVICE) + 3)
    len_date = " " * (len_max - len(Msg.DATE) + 3)
    len_time = " " * (len_max - len(Msg.TIME) + 3)
    len_contact = " " * (len_max - len(Msg.CONTACT) + 3)
    len_name = " " * (len_max - len(Msg.NAME) + 3)
    len_cost = " " * (len_max - len(Msg.COST) + 3)

    return f"<code>{Msg.CATEGORY}:{len_category}</code>{register[4]}\n" \
           f"<code>{Msg.SERVICE}:{len_service}</code>{register[5]}\n" \
           f"<code>{Msg.COST}:{len_cost}</code>{register[6]} {get_by_country(COUNTRY)[0]}\n" \
           f"<code>{Msg.DATE}:{len_date}</code>{register[7].date().strftime('%d.%m.%Y')}\n" \
           f"<code>{Msg.TIME}:{len_time}</code>{register[7].time().strftime('%H:%M')} - {register[8].time().strftime('%H:%M')}\n" \
           f"<code>{Msg.NAME}:{len_name}</code>{register[2]}\n" \
           f"<code>{Msg.CONTACT}:{len_contact}</code>{register[3]}\n"


async def register_msg_builder_client(state: dict) -> str:
    category = '-'
    if state.get('categories') != 0:
        for categories in state['categories']:
            category = f'{category}, {categories[1]}'

    service = '-'
    if len(state.get('services')) != 0:
        for services in state.get('services'):
            service = f'{service}, {services[1]}'

    date = '-'
    if state.get('date') is not None and state.get('date') != '-':
        date = datetime.strptime(state.get('date'), '%Y-%m-%d').date().strftime('%d.%m.%Y')

    time = '-'
    if state.get('start_time') is not None and state.get('start_time') != '-':
        time = datetime.strptime(state.get('start_time'), '%H:%M').time().strftime('%H:%M')
        if state.get('stop_time') is not None and state.get('stop_time') != '-':
            stop_time = datetime.strptime(state.get('stop_time'), '%H:%M').time().strftime('%H:%M')
            time = f'{time} - {stop_time}'

    client_contact, client_name = '-', '-'
    if '-' != state.get('client') is not None:
        client_contact = state.get('client')[3]
        client_name = state.get('client')[2]

    cost = '-'
    if '-' != state.get('cost') is not None:
        cost = f'{state.get("cost")} {get_by_country(COUNTRY)[0]}'

    len_max = max(
        [len(Msg.MASTER),
         len(Msg.CATEGORY),
         len(Msg.SERVICE),
         len(Msg.DATE),
         len(Msg.TIME),
         len(Msg.CONTACT),
         len(Msg.NAME),
         len(Msg.COST)])

    len_category = " " * (len_max - len(Msg.CATEGORY) + 3)
    len_service = " " * (len_max - len(Msg.SERVICE) + 3)
    len_date = " " * (len_max - len(Msg.DATE) + 3)
    len_time = " " * (len_max - len(Msg.TIME) + 3)
    len_contact = " " * (len_max - len(Msg.CONTACT) + 3)
    len_name = " " * (len_max - len(Msg.NAME) + 3)
    len_cost = " " * (len_max - len(Msg.COST) + 3)

    return f"{Title.NEW_REGISTER}" \
           f"<code>{Msg.CATEGORY}:{len_category}</code>{category if category == '-' else category[3:]}\n" \
           f"<code>{Msg.SERVICE}:{len_service}</code>{service if service == '-' else service[3:]}\n" \
           f"<code>{Msg.COST}:{len_cost}</code>{cost}\n" \
           f"<code>{Msg.DATE}:{len_date}</code>{date}\n" \
           f"<code>{Msg.TIME}:{len_time}</code>{time}\n" \
           f"<code>{Msg.NAME}:{len_name}</code>{client_name}\n" \
           f"<code>{Msg.CONTACT}:{len_contact}</code>{client_contact}\n"


async def register_msg_builder_client_db(register: tuple) -> str:

    len_max = max(
        [len(Msg.MASTER),
         len(Msg.CATEGORY),
         len(Msg.SERVICE),
         len(Msg.DATE),
         len(Msg.TIME),
         len(Msg.CONTACT),
         len(Msg.NAME),
         len(Msg.COST)])

    len_master = " " * (len_max - len(Msg.MASTER) + 3)
    len_category = " " * (len_max - len(Msg.CATEGORY) + 3)
    len_service = " " * (len_max - len(Msg.SERVICE) + 3)
    len_date = " " * (len_max - len(Msg.DATE) + 3)
    len_time = " " * (len_max - len(Msg.TIME) + 3)
    len_contact = " " * (len_max - len(Msg.CONTACT) + 3)
    len_name = " " * (len_max - len(Msg.NAME) + 3)
    len_cost = " " * (len_max - len(Msg.COST) + 3)

    return f"<code>{Msg.MASTER}:{len_master}</code>{register[2]}\n" \
           f"<code>{Msg.CATEGORY}:{len_category}</code>{register[5]}\n" \
           f"<code>{Msg.SERVICE}:{len_service}</code>{register[6]}\n" \
           f"<code>{Msg.COST}:{len_cost}</code>{register[7]}\n" \
           f"<code>{Msg.DATE}:{len_date}</code>{register[8].date().strftime('%d.%m.%Y')}\n" \
           f"<code>{Msg.TIME}:{len_time}</code>{register[8].time().strftime('%H:%M')} - {register[9].time().strftime('%H:%M')}\n" \
           f"<code>{Msg.NAME}:{len_name}</code>{register[3]}\n" \
           f"<code>{Msg.CONTACT}:{len_contact}</code>{register[4]}\n"
