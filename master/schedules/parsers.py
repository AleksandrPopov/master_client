import datetime

from master.schedules import db
from master.schedules.strings import Btn


async def schedule_msg(master_id: int, day: int = 0) -> str:
    schedules = await db.get_schedules(master_id=master_id)
    msg = ''
    len_max = max(len(day) for day in Btn.DAYS_LONG)

    for schedule in schedules:
        res = " " * (len_max - len(Btn.DAYS_LONG[schedule[0]]) + 6)
        schedule_day, start_time, stop_time = schedule[0], schedule[1], schedule[2]
        if schedule_day == day:
            if start_time == datetime.time.min and stop_time == datetime.time.min:
                msg += f"<code>{Btn.DAYS_LONG[schedule_day]}:{res[3:]}=> {Btn.DAY_OFF}</code>\n"
            else:
                msg += f"<code>{Btn.DAYS_LONG[schedule_day]}:{res[3:]}" \
                       f"=> {start_time.strftime('%H:%M')}-{stop_time.strftime('%H:%M')}</code>\n"
        else:
            if start_time == datetime.time.min and stop_time == datetime.time.min:
                msg += f"<code>{Btn.DAYS_LONG[schedule_day]}:{res}{Btn.DAY_OFF}</code>\n"
            else:
                msg += f"<code>{Btn.DAYS_LONG[schedule_day]}:{res}" \
                       f"{start_time.strftime('%H:%M')}-{stop_time.strftime('%H:%M')}</code>\n"
    return msg
