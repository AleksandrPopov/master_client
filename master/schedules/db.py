from datetime import datetime

from sqlalchemy import select, update, and_

from database.connector import engine
from database.tables import schedules


async def get_schedule_day(master_id: int, day: int) -> tuple:
    with engine.connect() as db:
        query = (
            select(
                schedules.c.start_time,
                schedules.c.stop_time
            ).
            where(
                and_(schedules.c.masters_id_pk == master_id,
                     schedules.c.day == day)
            ).
            order_by(schedules.c.day)
        )
        return db.execute(query).fetchone()


async def get_schedules(master_id: int) -> list:
    with engine.connect() as db:
        query = (
            select(
                schedules.c.day,
                schedules.c.start_time,
                schedules.c.stop_time
            ).
            where(schedules.c.masters_id_pk == master_id).
            order_by(schedules.c.day)
        )
        return db.execute(query).fetchall()


async def change_schedule_day(master_id: int, day: int, start: datetime.time, stop: datetime.time):
    with engine.connect() as db:
        db.execute(
            update(schedules).
            where(
                and_(schedules.c.masters_id_pk == master_id,
                     schedules.c.day == day)
            ).
            values(start_time=start, stop_time=stop)
        )
        db.commit()
