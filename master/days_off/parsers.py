import calendar
from datetime import datetime, timedelta

from master.days_off.strings import Msg


async def get_days_off(start: str, stop: str, date: datetime.date, days_off_db: list) -> list:
    start = datetime.strptime(start, '%d.%m.%Y').date() if start != Msg.EMPTY_DAY else start
    stop = datetime.strptime(stop, '%d.%m.%Y').date() if stop != Msg.EMPTY_DAY else stop

    month_calendar = calendar.monthcalendar(date.year, date.month)

    if len(days_off_db) != 0:
        for i in days_off_db:
            start_date = datetime.combine(i[0], datetime.min.time())
            stop_date = datetime.combine(i[1], datetime.min.time())

            result_date = stop_date - start_date
            duration = timedelta(days=result_date.days)

            for days in range(duration.days + 1):
                day = start_date + timedelta(days=days)

                for weeks in month_calendar:
                    for day_off in weeks:
                        if day_off == day.day and date.month == day.month and date.year == day.year:
                            weeks[day.weekday()] = 0

    if start != Msg.EMPTY_DAY:
        for weeks in month_calendar:
            for day in weeks:
                if day == start.day and date.month == start.month and date.year == start.year:
                    weeks[start.weekday()] = 0

    if start != Msg.EMPTY_DAY and stop != Msg.EMPTY_DAY:
        while stop > start:
            for weeks in month_calendar:
                for days in weeks:
                    if days == stop.day and date.month == stop.month and date.year == stop.year:
                        weeks[stop.weekday()] = 0
            stop = stop - timedelta(days=1)
    return month_calendar


async def days_off_parse(days_off_db: list):
    """Convert datetime.date to str"""
    days_off_list = []
    for day_off in days_off_db:
        start_date, stop_date = day_off[0], day_off[1]
        if start_date != stop_date:
            days_off_list.append(f"{start_date.strftime('%d.%m.%Y')} - "f"{stop_date.strftime('%d.%m.%Y')}")
        else:
            days_off_list.append(f"{start_date.strftime('%d.%m.%Y')}")
    return days_off_list
