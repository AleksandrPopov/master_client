import calendar
from datetime import datetime, timedelta
from math import ceil
import re

import phonenumbers

from config import COUNTRY, TZ
from client.add_register import db
from client.add_register.strings import Msg
from country_currencies import get_by_country

from master.registers.strings import Title


async def add_register_msg_builder(state: dict) -> str:
    master_name = '-'
    if state.get('master') is not None:
        master_name = state['master'][1]

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

    len_master = " " * (len_max - len(Msg.MASTER) + 3)
    len_category = " " * (len_max - len(Msg.CATEGORY) + 3)
    len_service = " " * (len_max - len(Msg.SERVICE) + 3)
    len_date = " " * (len_max - len(Msg.DATE) + 3)
    len_time = " " * (len_max - len(Msg.TIME) + 3)
    len_contact = " " * (len_max - len(Msg.CONTACT) + 3)
    len_name = " " * (len_max - len(Msg.NAME) + 3)
    len_cost = " " * (len_max - len(Msg.COST) + 3)

    if state.get('start') == 'masters':
        return f"<code>{Msg.MASTER}:{len_master}</code>{master_name}\n" \
               f"<code>{Msg.CATEGORY}:{len_category}</code>{category if category == '-' else category[3:]}\n" \
               f"<code>{Msg.SERVICE}:{len_service}</code>{service if service == '-' else service[3:]}\n" \
               f"<code>{Msg.COST}:{len_cost}</code>{cost}\n" \
               f"<code>{Msg.DATE}:{len_date}</code>{date}\n" \
               f"<code>{Msg.TIME}:{len_time}</code>{time}\n" \
               f"<code>{Msg.NAME}:{len_name}</code>{client_name}\n" \
               f"<code>{Msg.CONTACT}:{len_contact}</code>{client_contact}\n"
    else:
        return f"<code>{Msg.CATEGORY}:{len_category}</code>{category if category == '-' else category[3:]}\n" \
               f"<code>{Msg.SERVICE}:{len_service}</code>{service if service == '-' else service[3:]}\n" \
               f"<code>{Msg.COST}:{len_cost}</code>{cost}\n" \
               f"<code>{Msg.DATE}:{len_date}</code>{date}\n" \
               f"<code>{Msg.TIME}:{len_time}</code>{time}\n" \
               f"<code>{Msg.NAME}:{len_name}</code>{client_name}\n" \
               f"<code>{Msg.CONTACT}:{len_contact}</code>{client_contact}\n"


async def add_register_msg_builder_master(state: dict) -> str:
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

    len_max = max([
         len(Msg.CATEGORY),
         len(Msg.SERVICE),
         len(Msg.DATE),
         len(Msg.TIME),
         len(Msg.CONTACT),
         len(Msg.NAME),
         len(Msg.COST)
    ])

    len_category = " " * (len_max - len(Msg.CATEGORY) + 3)
    len_service = " " * (len_max - len(Msg.SERVICE) + 3)
    len_date = " " * (len_max - len(Msg.DATE) + 3)
    len_time = " " * (len_max - len(Msg.TIME) + 3)
    len_contact = " " * (len_max - len(Msg.CONTACT) + 3)
    len_name = " " * (len_max - len(Msg.NAME) + 3)
    len_cost = " " * (len_max - len(Msg.COST) + 3)

    return f"<code>{Title.NEW_REGISTER}" \
           f"<code>{Msg.CATEGORY}:{len_category}</code>{category if category == '-' else category[3:]}\n" \
           f"<code>{Msg.SERVICE}:{len_service}</code>{service if service == '-' else service[3:]}\n" \
           f"<code>{Msg.COST}:{len_cost}</code>{cost}\n" \
           f"<code>{Msg.DATE}:{len_date}</code>{date}\n" \
           f"<code>{Msg.TIME}:{len_time}</code>{time}\n" \
           f"<code>{Msg.NAME}:{len_name}</code>{client_name}\n" \
           f"<code>{Msg.CONTACT}:{len_contact}</code>{client_contact}\n"


async def price_msg_builder(master_id: int):
    msg_text = ''
    len_max = max([len(Msg.CATEGORY), len(Msg.NAME), len(Msg.COST), len(Msg.TIME)])

    category_len = " " * (len_max - len(Msg.CATEGORY) + 3)
    name_len = " " * (len_max - len(Msg.NAME) + 3)
    time_len = " " * (len_max - len(Msg.TIME) + 3)
    cost_len = " " * (len_max - len(Msg.COST) + 3)

    for category in await db.get_categories(master_id=master_id):
        for service in await db.get_service_data(category_id=category[0]):
            msg_text = f"{msg_text}\n" \
                       f"<code>{Msg.CATEGORY}:{category_len}</code><b>{category[1]}</b>\n" \
                       f"<code>{Msg.NAME}:{name_len}</code><b>{service[1]}</b>\n" \
                       f"<code>{Msg.TIME}:{time_len}</code><b>{await _time_parser(time=service[2])}</b>\n" \
                       f"<code>{Msg.COST}:{cost_len}</code><b>{service[3]} {get_by_country(COUNTRY)[0]}</b>\n"
    return msg_text


async def _time_parser(time: datetime) -> str:
    if time.hour != 0 and time.minute != 0:
        time = f"{time.hour} {Msg.HOUR} {time.minute} {Msg.MINUTES}"
    elif time.hour != 0 and time.minute == 0:
        time = f"{time.hour} {Msg.HOUR}"
    else:
        time = f"{time.minute} {Msg.MINUTES}"
    return time


async def exists_date(master_id, date: datetime.date, services: list) -> list:
    month_calendar = calendar.monthcalendar(year=date.year, month=date.month)

    days_off_db = await db.get_days_off(master_id=master_id, year=date.year, month=date.month)
    schedules_db = await db.get_schedules(master_id=master_id)
    registers_db = await db.get_registers_date(master_id=master_id, month=date.month, year=date.year)

    month_calendar = await _day_off_exists(days_off=days_off_db, calendar_list=month_calendar)
    month_calendar = await _schedules_exists(schedules=schedules_db, calendar_list=month_calendar)
    month_calendar = await _time_limit(services=services, schedules=schedules_db, calendar_list=month_calendar)
    month_calendar = await _days_list(date=date, calendar_list=month_calendar)
    if datetime.now().date() == date:
        month_calendar = await _day_now_exists(calendar_list=month_calendar, schedules=schedules_db)
    month_calendar = await _registers(
        schedule=schedules_db,
        services=services,
        registers=registers_db,
        calendar_list=month_calendar,
        date=date
    )

    return month_calendar


async def _registers(schedule: list, services: list, registers: list, calendar_list: list, date: datetime) -> list:
    date_now = datetime.now(TZ)
    # "flag" if registers doesn't exists in date now.
    flag = True
    for register in registers:
        # Date registers.
        date = register[0]
        # registers = await db.get_registers(master_id=master_id, date=date)

        # Change registers time when registers exists. Value '00:00:00'.
        day_schedule = await _schedule_time_list(schedule=schedule[date.weekday()])
        if date.date() == date_now.date():
            day_schedule = await _now_time_list(time_list=day_schedule)
            flag = False
        day_schedule = await _registers_time_list(
            time_list=day_schedule,
            services_list=services,
            schedule=schedule[date.weekday()],
            registers=registers
        )
        if len(set(day_schedule)) == 1:
            for i, day in enumerate(calendar_list):
                if day == date.day:
                    calendar_list[i] = 0

    if flag:
        day_schedule = await _schedule_time_list(schedule=schedule[date_now.weekday()])
        day_schedule = await _now_time_list(time_list=day_schedule)
        day_schedule = await _registers_time_list(
            time_list=day_schedule,
            services_list=services,
            schedule=schedule[date_now.weekday()],
            registers=registers
        )
        if len(set(day_schedule)) == 1:
            for i, day in enumerate(calendar_list):
                if day != 0:
                    date = datetime(year=date.year, month=date.month, day=day).date()
                    if date == date_now.date():
                        calendar_list[i] = 0

    return calendar_list


async def _day_now_exists(calendar_list: list, schedules: list) -> list:
    date_now = datetime.now(TZ)
    schedule = schedules[date_now.weekday()]
    stop_time = datetime.combine(date_now.date().min, schedule[2])
    if stop_time.time() != date_now.min.time():
        stop_time -= timedelta(minutes=30)
    for i, day in enumerate(calendar_list):
        if day == date_now.day and date_now.time() > stop_time.time():
            calendar_list[i] = 0
    return calendar_list


async def _day_off_exists(days_off: list, calendar_list: list) -> list:
    for i in days_off:
        start_date = i[0]
        stop_date = i[1]

        result_date = stop_date - start_date
        duration = timedelta(days=result_date.days)

        for days in range(duration.days + 1):
            day = start_date + timedelta(days=days)

            for weeks in calendar_list:
                for day_off in weeks:
                    if day_off == day.day:
                        weeks[day.weekday()] = 0
    return calendar_list


async def _schedules_exists(schedules: list, calendar_list: list) -> list:
    for schedule in schedules:
        day, start_time, stop_time = schedule[0], schedule[1], schedule[2]
        if start_time == stop_time:
            for week in calendar_list:
                week[day] = 0
    return calendar_list


async def _time_limit(services: list, schedules: list, calendar_list: list) -> list:
    services_time = datetime.now(TZ).min

    # Summ selected services time.
    # for service in services:
    #     time = datetime.strptime(service['time'], '%H:%M:%S')
    #     services_time += timedelta(hours=time.hour, minutes=time.minute)
    services_lt = await db.services_sum_time(services_ids=[i[0] for i in services])
    services_time += services_lt

    # Check schedule time.
    for schedule in schedules:
        day = schedule[0]
        start_time = datetime.combine(datetime.now().date(), schedule[1])
        stop_time = datetime.combine(datetime.now().date(), schedule[2])
        if start_time != stop_time:
            work_time = start_time - stop_time
            if work_time.days < 0:
                work_time = work_time + timedelta(days=1)
            work_time = datetime.now().min + work_time
            if services_time > work_time:
                for week in calendar_list:
                    week[day] = 0
    return calendar_list


async def _days_list(date: datetime, calendar_list: list) -> list:
    date_now = datetime.now().date()
    days_list = []

    for week in calendar_list:
        for calendar_day in week:
            if calendar_day == 0 or calendar_day < date_now.day and \
                    date.month == date_now.month and date.year == date_now.year:
                days_list.append(0)
                continue
            days_list.append(calendar_day)

    return days_list


async def time_exists(state: dict) -> list:
    date = datetime.strptime(state['date'], '%Y-%m-%d').date()
    schedule = await db.get_schedule(master_id=state['master'][0], day=date.weekday())
    registers = await db.get_registers(master_id=state['master'][0], date=date)

    day_schedule = await _schedule_time_list(schedule=schedule)
    if date == datetime.now(TZ).date():
        day_schedule = await _now_time_list(time_list=day_schedule)
    day_schedule = await _registers_time_list(
        time_list=day_schedule,
        services_list=state['services'],
        schedule=schedule,
        registers=registers
    )
    return day_schedule


async def _schedule_time_list(schedule: dict) -> list:
    time_list = []
    date = datetime.now().date().min

    start_time = datetime.combine(date, schedule[1])
    stop_time = datetime.combine(date, schedule[2])

    stop_time = stop_time + timedelta(days=1) if start_time > stop_time else stop_time

    # Create schedule.
    while start_time < stop_time:
        time_list.append(start_time)
        start_time += timedelta(minutes=30)

    # Adding empty time if the number of elements is not a multiple of 3.
    if len(time_list) % 3 == 1:
        time_list.append(start_time.min)
        time_list.append(start_time.min)

    if len(time_list) % 3 == 2:
        time_list.append(start_time.min)

    return time_list


async def _now_time_list(time_list: list) -> list:
    time_now = datetime.now(TZ)

    # Deleting the time if current time more than schedule.
    for i, time in enumerate(time_list):
        if time.time() < time_now.time():
            time_list[i] = time_now.min
    return time_list


async def _registers_time_list(time_list: list, services_list: list, schedule: dict, registers: list) -> list:
    service_time = await db.services_sum_time(services_ids=[i[0] for i in services_list])
    stop_schedule = datetime.combine(datetime.now().date().min, schedule[2])

    # Duration of services.
    # for service in services_list:
    #     time = service[2].split(':')
    #     service_time += timedelta(hours=int(time[0]), minutes=int(time[1]))

    # Deleting the time before stop schedule if the time is more than 30 minutes.
    for _ in range(ceil(service_time.seconds / 1800)):
        if stop_schedule in time_list:
            index = time_list.index(stop_schedule)
            time_list[index] = stop_schedule.min
        if stop_schedule != datetime.min:
            stop_schedule -= timedelta(minutes=30)

    # Duration of existing registers.
    for register in registers:
        start = datetime.combine(register[0].date().min, register[0].time())
        stop = datetime.combine(register[1].date().min, register[1].time())

        # Deleting the time of existing registers.
        start_temp = start
        while stop > start_temp:
            if start_temp in time_list:
                index = time_list.index(start_temp)
                time_list[index] = start_temp.min
            start_temp += timedelta(minutes=30)

        # Deleting the time before register if the time is more than 30 minutes.
        for _ in range(ceil(service_time.seconds / 1800) - 1):
            start -= timedelta(minutes=30)
            stop -= timedelta(minutes=30)

            if start in time_list:
                index = time_list.index(start)
                time_list[index] = start.min

    return time_list


async def cost_summ(services: list) -> int:
    summ = 0
    for service in services:
        summ += service[2]
    return int(summ)


async def cost_minus(cost: int, cost_service: int) -> str | int:
    cost -= cost_service
    if cost == 0:
        cost = '-'
    return int(cost)


async def time_summ(date: datetime, services: list):
    date += await db.services_sum_time(services_ids=[i[0] for i in services])
    return date.time().strftime('%H:%M')


async def sum_services_time(services: list) -> timedelta:
    services_time = timedelta(days=0)
    for service in services:
        time = service['time'].split(':')
        services_time += timedelta(hours=int(time[0]), minutes=int(time[1]))
    return services_time


async def format_contact(contact: str, country: str) -> str | bool:
    if contact[1:].isdigit() and phonenumbers.is_valid_number(phonenumbers.parse(contact, country)):
        return phonenumbers.format_number(phonenumbers.parse(contact, country), phonenumbers.PhoneNumberFormat.E164)
    else:
        return False


async def format_name(name: str) -> str | bool:
    """
    Remove unnecessary substrings and spaces.
    Checking the size of a string in bytes.

    :param
    :return:
    """
    name = name.lstrip(" ").rstrip(" ").lower()
    name = re.sub(" +", " ", name)
    name = re.sub("[<|>]", "", name).capitalize()
    if 64 > len(name.encode("utf-8")) != 0:
        return name
    else:
        return False

